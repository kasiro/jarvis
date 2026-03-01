// Modes Lua API: jarvis.modes

use mlua::{Lua, Table};
use crate::modes::ModesManager;
use crate::DB;

pub fn register(
    lua: &Lua,
    jarvis: &Table,
) -> mlua::Result<()> {
    let modes = lua.create_table()?;

    // @ jarvis.modes.set_mode(mode_name) -> bool
    // Переключить режим работы Jarvis
    let set_mode_fn = lua.create_function(move |_, mode_name: String| {
        // Get global SettingsManager
        let settings = DB.get()
            .ok_or_else(|| mlua::Error::runtime("Settings not initialized"))?;
        
        let modes_manager = ModesManager::new(settings);
        
        match modes_manager.set_mode(&mode_name, settings) {
            Ok(success) => {
                log::info!("[Lua] Mode set to: {}", mode_name);
                Ok(success)
            }
            Err(e) => {
                log::error!("[Lua] Failed to set mode: {}", e);
                Ok(false)
            }
        }
    })?;
    modes.set("set_mode", set_mode_fn)?;

    // @ jarvis.modes.get_current_mode() -> string
    // Получить текущий режим
    let get_current_mode_fn = lua.create_function(move |_, ()| {
        let settings = DB.get()
            .ok_or_else(|| mlua::Error::runtime("Settings not initialized"))?;
        
        let modes_manager = ModesManager::new(settings);
        let current = modes_manager.get_current_mode();
        log::debug!("[Lua] Current mode: {}", current);
        Ok(current)
    })?;
    modes.set("get_current_mode", get_current_mode_fn)?;

    // @ jarvis.modes.get_available_modes() -> table
    // Получить список доступных режимов
    let get_available_modes_fn = lua.create_function(move |_, ()| {
        let settings = DB.get()
            .ok_or_else(|| mlua::Error::runtime("Settings not initialized"))?;
        
        let modes_manager = ModesManager::new(settings);
        let modes_list = modes_manager.get_available_modes();
        log::debug!("[Lua] Available modes: {:?}", modes_list);
        Ok(modes_list)
    })?;
    modes.set("get_available_modes", get_available_modes_fn)?;

    jarvis.set("modes", modes)?;

    Ok(())
}
