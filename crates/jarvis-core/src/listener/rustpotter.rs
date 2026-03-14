use std::sync::Mutex;

use once_cell::sync::OnceCell;
use rustpotter::Rustpotter;

use crate::config;

// store rustpotter instance
static RUSTPOTTER: OnceCell<Mutex<Rustpotter>> = OnceCell::new();

pub fn init() -> Result<(), ()> {
    let rustpotter_config = config::RUSTPOTTER_DEFAULT_CONFIG;

    // create rustpotter instance
    match Rustpotter::new(&rustpotter_config) {
        Ok(mut rinstance) => {
            // success
            // wake word files list - load ALL available wake words for better detection
            let rustpotter_wake_word_files: [&str; 6] = [
                "resources/rustpotter/jarvis-default.rpw",
                "resources/rustpotter/jarvis-community-1.rpw",
                "resources/rustpotter/jarvis-community-2.rpw",
                "resources/rustpotter/jarvis-community-3.rpw",
                "resources/rustpotter/jarvis-community-4.rpw",
                "resources/rustpotter/jarvis-community-5.rpw",
            ];

            // load wake word files
            for rpw in rustpotter_wake_word_files {
                match rinstance.add_wakeword_from_file(rpw, rpw) {
                    Ok(_) => info!("🥒 Rustpotter: Loaded wake word '{}'", rpw),
                    Err(e) => error!("Failed to load wakeword file '{}': {}", rpw, e),
                }
            }

            // store
            let _ = RUSTPOTTER.set(Mutex::new(rinstance));
            info!("🥒 Rustpotter initialized with {} wake word(s)", rustpotter_wake_word_files.len());
        }
        Err(msg) => {
            error!("Rustpotter failed to initialize.\nError details: {}", msg);

            return Err(());
        }
    }

    Ok(())
}

pub fn data_callback(frame_buffer: &[i16]) -> Option<i32> {
    let mut lock = RUSTPOTTER.get().unwrap().lock();
    let rustpotter = lock.as_mut().unwrap();
    // let detection = rustpotter.process_samples(frame_buffer.to_vec()); // @TODO. Temp crutch. Fix optimization issue, frame_buffer should not be copied to a new vector!
    let detection = rustpotter.process_samples(frame_buffer);

    debug!("🥒 Rustpotter data_callback: frame_size={}", frame_buffer.len());

    if let Some(detection) = detection {
        // Always log detection for debugging
        debug!("Rustpotter score: {:.3} (threshold: {:.3})", detection.score, config::RUSPOTTER_MIN_SCORE);

        if detection.score > config::RUSPOTTER_MIN_SCORE {
            info!("🥒 Rustpotter WAKE WORD DETECTED! Score: {:.3}", detection.score);
            info!("Rustpotter detection info:\n{:?}", detection);

            return Some(0);
        } else {
            // Log low scores for debugging
            debug!("Rustpotter: score too low {:.3} < {:.3}", detection.score, config::RUSPOTTER_MIN_SCORE);
        }
    }

    None
}
