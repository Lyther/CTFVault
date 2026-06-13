// Конфигурация API для CapyAgro
// Этот файл содержит настройки для работы с API системы управления теплицей

window.API_CONFIG = {
    // API ключ для тестовой среды
    // ВНИМАНИЕ: В продакшене используйте безопасное хранение ключей!
    KEY: 'test_key_123',
    
    // Базовый URL для API
    ENDPOINT: '/api',
    
    // Эндпоинты
    ENDPOINTS: {
        sector: (id) => `/api/sector/${id}`,
        sectorStatus: (number) => `/api/v1/sectors/${number}/status`,
        adjustSector: (id) => `/api/sector/${id}/adjust`,
        rawCommand: '/api/v1/raw_command'
    }
};

// Функция для отправки запроса с API ключом
window.sendWithAPIKey = async function(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': window.API_CONFIG.KEY,
        ...options.headers
    };
    
    return fetch(url, {
        ...options,
        headers
    });
};
