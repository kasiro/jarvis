use std::sync::Arc;
use parking_lot::RwLock;
use serde::{Serialize, Deserialize};

use crate::db::structs::Settings;

/// Доступные режимы работы Jarvis
pub const MODES: &[&str] = &["normal", "kid", "dev"];

/// Событие смены режима
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModeChangedEvent {
    pub old: String,
    pub new: String,
}

/// Менеджер режимов работы Jarvis
/// Управляет переключением режимов и хранит текущее состояние
pub struct ModesManager {
    /// Текущий режим
    current_mode: RwLock<String>,
    /// Доступные режимы
    available_modes: Vec<String>,
}

impl ModesManager {
    /// Создать новый ModesManager с загрузкой режима из настроек
    pub fn new(settings: &Arc<RwLock<Settings>>) -> Self {
        let settings_read = settings.read();
        let current_mode = settings_read
            .get("mode")
            .unwrap_or_else(|| "normal".to_string());
        drop(settings_read);

        Self {
            current_mode: RwLock::new(current_mode),
            available_modes: MODES.iter().map(|s| s.to_string()).collect(),
        }
    }

    /// Переключить режим и сохранить в настройки
    /// Возвращает true если режим успешно переключен
    pub fn set_mode(&self, new_mode: &str, settings: &Arc<RwLock<Settings>>) -> Result<bool, String> {
        // Валидация режима
        if !self.available_modes.contains(&new_mode.to_string()) {
            return Err(format!("Invalid mode: {}. Available modes: {:?}", new_mode, self.available_modes));
        }

        let mut current = self.current_mode.write();
        
        // Если режим не изменился - ничего не делаем
        if *current == new_mode {
            return Ok(true);
        }

        let old_mode = current.clone();
        
        // Обновляем текущий режим
        *current = new_mode.to_string();
        drop(current);

        // Сохраняем в настройки
        {
            let mut settings_write = settings.write();
            settings_write
                .set("mode", new_mode)
                .map_err(|e| format!("Failed to save mode to settings: {}", e))?;
            drop(settings_write);
        }

        // Логируем смену режима
        log::info!("Mode changed: {} -> {}", old_mode, new_mode);

        // Здесь можно добавить публикацию события в EventBus
        // self.event_bus.publish("mode_changed", ModeChangedEvent { old: old_mode, new: new_mode.to_string() }).await;

        Ok(true)
    }

    /// Получить текущий режим
    pub fn get_current_mode(&self) -> String {
        self.current_mode.read().clone()
    }

    /// Получить список доступных режимов
    pub fn get_available_modes(&self) -> Vec<String> {
        self.available_modes.clone()
    }

    /// Проверить, является ли режим допустимым
    pub fn is_valid_mode(&self, mode: &str) -> bool {
        self.available_modes.contains(&mode.to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_modes_constant() {
        assert!(MODES.contains(&"normal"));
        assert!(MODES.contains(&"kid"));
        assert!(MODES.contains(&"dev"));
        assert_eq!(MODES.len(), 3);
    }

    #[test]
    fn test_is_valid_mode() {
        let settings = Arc::new(RwLock::new(Settings::default()));
        let manager = ModesManager::new(&settings);

        assert!(manager.is_valid_mode("normal"));
        assert!(manager.is_valid_mode("kid"));
        assert!(manager.is_valid_mode("dev"));
        assert!(!manager.is_valid_mode("invalid"));
    }

    #[test]
    fn test_get_current_mode() {
        let settings = Arc::new(RwLock::new(Settings::default()));
        let manager = ModesManager::new(&settings);

        // По умолчанию должен быть "normal"
        assert_eq!(manager.get_current_mode(), "normal");
    }

    #[test]
    fn test_get_available_modes() {
        let settings = Arc::new(RwLock::new(Settings::default()));
        let manager = ModesManager::new(&settings);

        let modes = manager.get_available_modes();
        assert_eq!(modes.len(), 3);
        assert!(modes.contains(&"normal".to_string()));
        assert!(modes.contains(&"kid".to_string()));
        assert!(modes.contains(&"dev".to_string()));
    }

    #[test]
    fn test_set_mode() {
        let settings = Arc::new(RwLock::new(Settings::default()));
        let manager = ModesManager::new(&settings);

        // Переключаем в kid mode
        assert!(manager.set_mode("kid", &settings).is_ok());
        assert_eq!(manager.get_current_mode(), "kid");

        // Переключаем в dev mode
        assert!(manager.set_mode("dev", &settings).is_ok());
        assert_eq!(manager.get_current_mode(), "dev");

        // Возвращаем в normal
        assert!(manager.set_mode("normal", &settings).is_ok());
        assert_eq!(manager.get_current_mode(), "normal");
    }

    #[test]
    fn test_set_invalid_mode() {
        let settings = Arc::new(RwLock::new(Settings::default()));
        let manager = ModesManager::new(&settings);

        let result = manager.set_mode("invalid_mode", &settings);
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("Invalid mode"));
    }

    #[test]
    fn test_set_same_mode() {
        let settings = Arc::new(RwLock::new(Settings::default()));
        let manager = ModesManager::new(&settings);

        // Установка того же режима должна возвращать true
        assert!(manager.set_mode("normal", &settings).is_ok());
        assert_eq!(manager.get_current_mode(), "normal");
    }
}
