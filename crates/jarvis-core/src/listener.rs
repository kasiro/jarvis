mod vosk;

#[cfg(feature = "rustpotter_wake")]
mod rustpotter;

use once_cell::sync::OnceCell;

use crate::config::structs::WakeWordEngine;

use crate::DB;

static WAKE_WORD_ENGINE: OnceCell<WakeWordEngine> = OnceCell::new();

pub fn init() -> Result<(), String> {
    if WAKE_WORD_ENGINE.get().is_some() {
        return Ok(());
    }

    let engine = DB.get().unwrap().read().wake_word_engine;

    WAKE_WORD_ENGINE.set(engine)
        .map_err(|_| "Wake word engine already set".to_string())?;

    match engine {
        WakeWordEngine::Porcupine => {
            Err("Porcupine wake-word engine is not supported".to_string())
        }
        WakeWordEngine::Rustpotter => {
            #[cfg(feature = "rustpotter_wake")]
            {
                info!("Initializing Rustpotter wake-word engine.");
                rustpotter::init()
                    .map_err(|_| "Failed to init Rustpotter".to_string())
            }
            #[cfg(not(feature = "rustpotter_wake"))]
            {
                Err("Rustpotter wake-word engine is not enabled. Enable the 'rustpotter_wake' feature.".to_string())
            }
        }
        WakeWordEngine::Vosk => {
            info!("Initializing Vosk as wake-word engine.");
            warn!("Using Vosk as wake-word engine is highly not recommended, because it's very slow for this task.");
            vosk::init()
                .map_err(|_| "Failed to init Vosk".to_string())
        }
    }
}

pub fn data_callback(frame_buffer: &[i16]) -> Option<i32> {
    match WAKE_WORD_ENGINE.get()? {
        WakeWordEngine::Porcupine => None,
        #[cfg(feature = "rustpotter_wake")]
        WakeWordEngine::Rustpotter => rustpotter::data_callback(frame_buffer),
        #[cfg(not(feature = "rustpotter_wake"))]
        WakeWordEngine::Rustpotter => None,
        WakeWordEngine::Vosk => vosk::data_callback(frame_buffer),
    }
}
