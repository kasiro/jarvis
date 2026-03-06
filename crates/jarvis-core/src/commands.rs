use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::fs;
use std::time::Duration;
use std::process::{Child, Command};

use seqdiff::ratio;

mod structs;
pub use structs::*;

use parking_lot::RwLock;
use crate::{config, i18n, audio, APP_DIR};

#[cfg(feature = "lua")]
use crate::lua::{self, SandboxLevel, CommandContext};

pub fn parse_commands() -> Result<Vec<JCommandsList>, String> {
    let mut commands: Vec<JCommandsList> = Vec::new();

    let commands_path = APP_DIR.join(config::COMMANDS_PATH);
    let cmd_dirs = fs::read_dir(&commands_path)
        .map_err(|e| format!("Error reading commands directory {:?}: {}", commands_path, e))?;

    for entry in cmd_dirs.flatten() {
        let cmd_path = entry.path();
        
        // Пробуем найти command.toml или command.yaml
        let toml_file = cmd_path.join("command.toml");
        let yaml_file = cmd_path.join("command.yaml");

        let content: String;
        let is_toml: bool;

        if toml_file.exists() {
            content = match fs::read_to_string(&toml_file) {
                Ok(c) => c,
                Err(e) => {
                    warn!("Failed to read {}: {}", toml_file.display(), e);
                    continue;
                }
            };
            is_toml = true;
        } else if yaml_file.exists() {
            content = match fs::read_to_string(&yaml_file) {
                Ok(c) => c,
                Err(e) => {
                    warn!("Failed to read {}: {}", yaml_file.display(), e);
                    continue;
                }
            };
            is_toml = false;
        } else {
            // Нет ни command.toml ни command.yaml
            continue;
        }

        // Парсим в зависимости от формата
        let file: JCommandsList = if is_toml {
            match toml::from_str(&content) {
                Ok(f) => f,
                Err(e) => {
                    warn!("Failed to parse TOML {}: {}", toml_file.display(), e);
                    continue;
                }
            }
        } else {
            // YAML legacy format - нужно конвертировать
            // YAML имеет структуру: { list: [ {...}, ... ] }
            match serde_yaml::from_str::<serde_yaml::Value>(&content) {
                Ok(value) => {
                    // Достаём list поле
                    let list_value = value.get("list").or_else(|| value.get("commands"));
                    
                    let legacy_commands: Vec<LegacyCommand> = if let Some(list) = list_value {
                        match serde_yaml::from_value(list.clone()) {
                            Ok(cmds) => cmds,
                            Err(e) => {
                                warn!("Failed to parse YAML list {}: {}", yaml_file.display(), e);
                                continue;
                            }
                        }
                    } else if value.as_sequence().is_some() {
                        // Если это прямой массив
                        match serde_yaml::from_value(value.clone()) {
                            Ok(cmds) => cmds,
                            Err(e) => {
                                warn!("Failed to parse YAML as array {}: {}", yaml_file.display(), e);
                                continue;
                            }
                        }
                    } else {
                        warn!("Failed to parse YAML {}: invalid structure", yaml_file.display());
                        continue;
                    };
                    
                    // Конвертируем legacy YAML в JCommand
                    let mut commands = Vec::new();
                    for (idx, legacy) in legacy_commands.iter().enumerate() {
                        let mut sounds_map = HashMap::new();
                        let mut phrases_map = HashMap::new();
                        
                        // Convert voice.sounds
                        if let Some(voice) = &legacy.voice {
                            sounds_map.insert("ru".to_string(), voice.sounds.clone());
                        }
                        
                        // Convert phrases
                        if let Some(phrases) = &legacy.phrases {
                            phrases_map.insert("ru".to_string(), phrases.clone());
                        }

                        let cmd = JCommand {
                            id: format!("{}_{}_{}",
                                cmd_path.file_name().unwrap().to_string_lossy(),
                                legacy.command.action,
                                idx
                            ),
                            cmd_type: legacy.command.action.clone(),
                            description: String::new(),
                            exe_path: legacy.command.exe_path.clone(),
                            exe_args: legacy.command.exe_args.clone(),
                            cli_cmd: legacy.command.cli_cmd.clone(),
                            cli_args: legacy.command.cli_args.clone(),
                            env: HashMap::new(),
                            script: legacy.command.script.clone(),  // ✅ КОПИРУЕМ script из YAML
                            sandbox: String::new(),
                            timeout: 10000,
                            sounds: sounds_map,
                            phrases: phrases_map,
                            slots: HashMap::new(),
                            sounds_cache: RwLock::new(HashMap::new()),
                            phrases_cache: RwLock::new(HashMap::new()),
                        };
                        commands.push(cmd);
                    }
                    JCommandsList {
                        path: cmd_path.clone(),
                        commands,
                    }
                }
                Err(e) => {
                    warn!("Failed to parse YAML {}: {}", yaml_file.display(), e);
                    continue;
                }
            }
        };

        commands.push(JCommandsList {
            path: cmd_path,
            commands: file.commands,
        });
    }

    if commands.is_empty() {
        Err("No commands found".into())
    } else {
        info!("Loaded {} command pack(s)", commands.len());
        Ok(commands)
    }
}


pub fn commands_hash(commands: &[JCommandsList]) -> String {
    use sha2::{Sha256, Digest};
    
    let mut hasher = Sha256::new();
    
    let lang = i18n::get_language();
    hasher.update(lang.as_bytes());
    hasher.update(b"|");

    // collect all command ids and phrases for current language, sorted
    let mut all_data: Vec<(&str, _)> = commands.iter()
        .flat_map(|ac| ac.commands.iter().map(|c| (c.id.as_str(), c.get_phrases(&lang))))
        .collect();
    all_data.sort_by_key(|(id, _)| *id);
    
    for (id, phrases) in all_data {
        hasher.update(id.as_bytes());
        for phrase in phrases.iter() {
            hasher.update(phrase.as_bytes());
        }
    }
    
    format!("{:x}", hasher.finalize())
}


pub fn fetch_command<'a>(
    phrase: &str,
    commands: &'a [JCommandsList],
) -> Option<(&'a PathBuf, &'a JCommand)> {
    let lang = i18n::get_language();

    let phrase = phrase.trim().to_lowercase();
    if phrase.is_empty() {
        return None;
    }

    let phrase_chars: Vec<char> = phrase.chars().collect();
    let phrase_words: Vec<&str> = phrase.split_whitespace().collect();

    let mut result: Option<(&PathBuf, &JCommand)> = None;
    let mut best_score = config::CMD_RATIO_THRESHOLD;

    for cmd_list in commands {
        for cmd in &cmd_list.commands {
            let cmd_phrases = cmd.get_phrases(&lang);
            
            for cmd_phrase in cmd_phrases.iter() {
                let cmd_phrase_lower = cmd_phrase.trim().to_lowercase();
                let cmd_phrase_chars: Vec<char> = cmd_phrase_lower.chars().collect();
                
                // character-level similarity
                let char_ratio = ratio(&phrase_chars, &cmd_phrase_chars);
                
                // word-level similarity
                let cmd_words: Vec<&str> = cmd_phrase_lower.split_whitespace().collect();
                let word_score = word_overlap_score(&phrase_words, &cmd_words);
                
                // combined score
                let score = (char_ratio * 0.6) + (word_score * 0.4);
                
                // early exit on perfect match
                if score >= 99.0 {
                    debug!("Perfect match: '{}' -> '{}'", phrase, cmd_phrase_lower);
                    return Some((&cmd_list.path, cmd));
                }

                if score >= best_score {
                    best_score = score;
                    result = Some((&cmd_list.path, cmd));
                }
            }
        }
    }

    if let Some((_, cmd)) = result {
        info!("Fuzzy match: '{}' -> cmd '{}' (score: {:.1}%)", phrase, cmd.id, best_score);
    } else {
        debug!("No match for '{}' (best: {:.1}%)", phrase, best_score);
    }
    
    result
}


fn word_overlap_score(input_words: &[&str], cmd_words: &[&str]) -> f64 {
    if input_words.is_empty() || cmd_words.is_empty() {
        return 0.0;
    }

    let mut matched = 0.0;
    
    // pre-compute cmd word chars to avoid repeated allocations
    let cmd_word_chars: Vec<Vec<char>> = cmd_words
        .iter()
        .map(|w| w.chars().collect())
        .collect();
    
    for input_word in input_words {
        let input_chars: Vec<char> = input_word.chars().collect();
        
        let best_word_match = cmd_word_chars
            .iter()
            .map(|cw| ratio(&input_chars, cw))
            .fold(0.0_f64, f64::max);
        
        if best_word_match > 70.0 {
            matched += best_word_match / 100.0;
        }
    }

    let max_words = input_words.len().max(cmd_words.len()) as f64;
    (matched / max_words) * 100.0
}




pub fn execute_exe(exe: &str, args: &[String]) -> std::io::Result<Child> {
    Command::new(exe).args(args).spawn()
}

pub fn execute_cli(cmd: &str, args: &[String], env: &HashMap<String, String>) -> std::io::Result<Child> {
    if cfg!(target_os = "windows") {
        debug!("Spawning: cmd /C {} {:?}", cmd, args);
        Command::new("cmd").arg("/C").arg(cmd).args(args).envs(env).spawn()
    } else {
        // On Linux, if args start with -c, the command is already a shell command
        // so we execute it directly without wrapping in another shell
        if args.first().map_or(false, |a| a == "-c") {
            debug!("Spawning: {} {:?}", cmd, args);
            Command::new(cmd).args(args).envs(env).spawn()
        } else {
            debug!("Spawning: sh -c {} {:?}", cmd, args);
            Command::new("sh").arg("-c").arg(cmd).args(args).envs(env).spawn()
        }
    }
}

pub fn execute_command(cmd_path: &PathBuf, cmd_config: &JCommand, phrase: Option<&str>, slots: Option<&HashMap<String, SlotValue>>) -> Result<bool, String> {
    // execute command by the type
    match cmd_config.cmd_type.as_str() {

        // VOICE command - play sounds only
        // IMPORTANT: voice commands should NOT chain to avoid duplicate execution
        "voice" => {
            // Get sounds for current language
            let lang = i18n::get_language();
            let sounds = cmd_config.get_sounds(&lang);

            // Play first sound if available
            if let Some(sound_name) = sounds.first() {
                // Get sound file path
                if let Some(sound_dir) = audio::get_sound_directory() {
                    // Sounds are in {voice}/{lang}/{sound_name}.mp3
                    let sound_path = sound_dir.join(&lang).join(format!("{}.mp3", sound_name));

                    if sound_path.exists() {
                        info!("Playing voice sound: {}", sound_path.display());
                        audio::play_sound(&sound_path);
                        // Return false to disable chaining - prevents duplicate voice commands!
                        return Ok(false);
                    } else {
                        warn!("Voice sound not found: {}", sound_path.display());
                    }
                }
            }

            // No sounds found, but still success
            // Return false to disable chaining
            Ok(false)
        }

        // LUA command
        #[cfg(feature = "lua")]
        "lua" => {
            execute_lua_command(cmd_path, cmd_config, phrase, slots)
        }

        // AutoHotkey command
        // @TODO: Consider adding ahk source files execution?
        "ahk" => {
            let exe_path_absolute = Path::new(&cmd_config.exe_path);
            let exe_path_local = cmd_path.join(&cmd_config.exe_path);

            let exe_path = if exe_path_absolute.exists() {
                exe_path_absolute
            } else {
                exe_path_local.as_path()
            };

            execute_exe(exe_path.to_str().unwrap(), &cmd_config.exe_args)
                .map(|_| true)
                .map_err(|e| format!("AHK process spawn error: {}", e))
        }

        // CLI command type
        // @TODO: Consider security restrictions
        "cli" => {
            // Resolve environment variable placeholders
            let mut resolved_env = HashMap::new();
            for (key, value) in &cmd_config.env {
                let resolved = resolve_env_placeholder(phrase, slots, value);
                if !resolved.is_empty() {
                    resolved_env.insert(key.clone(), resolved);
                }
            }

            execute_cli(&cmd_config.cli_cmd, &cmd_config.cli_args, &resolved_env)
                .map(|_| true)
                .map_err(|e| format!("CLI command error: {}", e))
        }
        
        // TERMINATOR command (T1000)
        "terminate" => {
            std::thread::sleep(Duration::from_secs(2));
            std::process::exit(0);
        }
        
        // STOP CHANING
        "stop_chaining" => Ok(false),

        // PYTHON script
        "python" => {
            #[cfg(feature = "python")]
            {
                execute_python(cmd_path, cmd_config, phrase, slots)
            }
            #[cfg(not(feature = "python"))]
            {
                error!("Python support not enabled");
                Err("Python support not enabled".to_string())
            }
        }

        // other
        _ => {
            error!("Command type unknown: {}", cmd_config.cmd_type);
            Err(format!("Command type unknown: {}", cmd_config.cmd_type).into())
        }
    }
}

// look up a command by its ID
pub fn get_command_by_id<'a>(
    commands: &'a [JCommandsList],
    id: &str,
) -> Option<(&'a PathBuf, &'a JCommand)> {
    for cmd_list in commands {
        for cmd in &cmd_list.commands {
            if cmd.id == id {
                return Some((&cmd_list.path, cmd));
            }
        }
    }
    None
}

pub fn list_paths(commands: &[JCommandsList]) -> Vec<&Path> {
    commands.iter().map(|x| x.path.as_path()).collect()
}

#[cfg(feature = "lua")]
fn execute_lua_command(
    cmd_path: &PathBuf,
    cmd_config: &JCommand,
    phrase: Option<&str>,
    slots: Option<&HashMap<String, SlotValue>>
) -> Result<bool, String> {
    // get script path

    let script_name = if cmd_config.script.is_empty() {
        "script.lua"
    } else {
        &cmd_config.script
    };

    let script_path = cmd_path.join(script_name);

    if !script_path.exists() {
        return Err(format!("Lua script not found: {}", script_path.display()));
    }

    // parse sandbox level
    let sandbox = SandboxLevel::from_str(&cmd_config.sandbox);

    // create context
    let context = CommandContext {
        phrase: phrase.unwrap_or("").to_string(),
        command_id: cmd_config.id.clone(),
        command_path: cmd_path.clone(),
        language: i18n::get_language(),
        slots: slots.map(|s| s.clone()),
    };

    // get timeout
    let timeout = Duration::from_millis(cmd_config.timeout);

    info!("Executing Lua command: {} (sandbox: {:?}, timeout: {:?})",
          cmd_config.id, sandbox, timeout);

    // execute
    match lua::execute(&script_path, context, sandbox, timeout) {
        Ok(result) => {
            info!("Lua command {} completed (chain: {})", cmd_config.id, result.chain);
            Ok(result.chain)
        }
        Err(e) => {
            error!("Lua command {} failed: {}", cmd_config.id, e);
            Err(e.to_string())
        }
    }
}

// Resolve environment variable placeholders like ${city|default} and ${lang}
fn resolve_env_placeholder(
    _phrase: Option<&str>,
    slots: Option<&HashMap<String, SlotValue>>,
    value: &str,
) -> String {
    let mut result = value.to_string();
    
    // Replace ${lang} with current language
    result = result.replace("${lang}", &i18n::get_language());
    
    // Replace ${city|default} with city from slots or default
    if let Some(slots) = slots {
        if let Some(SlotValue::Text(city)) = slots.get("city") {
            // Extract default value from placeholder if present
            if let Some(start) = value.find("${city|") {
                if let Some(end) = value[start..].find('}') {
                    let default_start = start + "${city|".len();
                    let _default_val = &value[default_start..start + end];
                    result = result.replace(&value[start..=start + end], city);
                    return result;
                }
            }
            // Simple ${city} replacement
            result = result.replace("${city}", city);
        }
    }
    
    // Replace remaining placeholders with their default values
    // Pattern: ${name|default} -> default
    while let Some(start) = result.find("${") {
        if let Some(end) = result[start..].find('}') {
            let placeholder_end = start + end;
            let placeholder = &result[start..=placeholder_end];
            
            // Extract default value
            if let Some(pipe_pos) = result[start..placeholder_end].find('|') {
                let default_start = start + pipe_pos + 1;
                let default_val = &result[default_start..placeholder_end];
                result = result.replace(placeholder, default_val);
            } else {
                // No default, remove placeholder
                result = result.replace(placeholder, "");
            }
        } else {
            break;
        }
    }

    result
}

#[cfg(feature = "python")]
fn execute_python(
    cmd_path: &PathBuf,
    cmd_config: &JCommand,
    phrase: Option<&str>,
    slots: Option<&HashMap<String, SlotValue>>,
) -> Result<bool, String> {
    use std::process::{Command, Stdio};
    use std::io::Write;
    use serde_json::{json, Value};

    // Get script path
    let script_name = if cmd_config.script.is_empty() {
        "script.py"
    } else {
        &cmd_config.script
    };

    let script_path = cmd_path.join(script_name);

    if !script_path.exists() {
        return Err(format!("Python script not found: {}", script_path.display()));
    }

    info!("Executing Python script: {}", script_path.display());

    // Get relative path from resources/commands
    let relative_path = script_path.strip_prefix(APP_DIR.join("resources/commands"))
        .map_err(|_| "Invalid script path")?;
    let module_path = relative_path.to_str()
        .ok_or("Invalid script path")?
        .trim_end_matches(".py")
        .replace("/", ".");

    // Create context JSON
    let context = json!({
        "phrase": phrase.unwrap_or(""),
        "language": i18n::get_language(),
        "slots": slots.map(|s| {
            s.iter().map(|(k, v)| {
                (k.clone(), match v {
                    SlotValue::Text(t) => json!(t),
                    SlotValue::Number(n) => json!(n),
                })
            }).collect::<HashMap<_, _>>()
        }).unwrap_or_default(),
        "command_path": cmd_path.to_str().unwrap_or(""),
        "module": module_path,
    });

    // Spawn Python server via uv run from project root (uses root .venv)
    // Добавляем resources/commands в PYTHONPATH для импорта jarvis_server
    let mut child = Command::new("uv")
        .args(["run", "--with", "aiohttp", "python", "-m", "jarvis_server"])
        .current_dir(&*APP_DIR)  // Запуск из корня проекта (дереференсим Lazy<PathBuf>)
        .env("PYTHONPATH", APP_DIR.join("resources/commands"))  // Добавляем путь к модулям
        .env("RUST_LOG", "off")  // Отключаем Rust логи в stderr
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())  // Игнорируем stderr (логи идут в лог Jarvis)
        .spawn()
        .map_err(|e| format!("Failed to spawn Python: {}", e))?;

    // Send context via stdin
    let context_json = context.to_string();
    if let Some(ref mut stdin) = child.stdin {
        stdin.write_all(context_json.as_bytes())
            .map_err(|e| format!("Failed to send context: {}", e))?;
        stdin.write_all(b"\n")
            .map_err(|e| format!("Failed to send newline: {}", e))?;
    }

    // Read response
    let output = child.wait_with_output()
        .map_err(|e| format!("Failed to read output: {}", e))?;

    // Parse response
    let response: Value = serde_json::from_slice(&output.stdout)
        .map_err(|e| format!("Failed to parse response: {}", e))?;

    // Check result
    let success = response.get("success").and_then(|v| v.as_bool()).unwrap_or(false);
    
    if !success {
        let error = response.get("error").and_then(|v| v.as_str()).unwrap_or("Unknown error");
        error!("Python script error: {}", error);
        return Err(format!("Python script error: {}", error));
    }

    info!("Python script executed successfully");
    Ok(true)
}