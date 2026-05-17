// Работа с localStorage

// Ключи для localStorage
const STORAGE_KEYS = {
    USER_ID: 'kiip_user_id',
    SUBSCRIPTION: 'kiip_subscription',
    KEY: 'kiip_key',
    PROGRESS: 'kiip_progress'
};

// Получение DeviceID
function getDeviceID() {
    return localStorage.getItem(STORAGE_KEYS.USER_ID);
}

// Проверка подписки
function hasSubscription() {
    const subscription = localStorage.getItem(STORAGE_KEYS.SUBSCRIPTION);
    return subscription === 'paid';
}

// Сохранение прогресса
function saveProgress(blockNumber, data) {
    const progress = JSON.parse(localStorage.getItem(STORAGE_KEYS.PROGRESS) || '{}');
    progress[`block${blockNumber}`] = data;
    localStorage.setItem(STORAGE_KEYS.PROGRESS, JSON.stringify(progress));
}

// Получение прогресса
function getProgress(blockNumber) {
    const progress = JSON.parse(localStorage.getItem(STORAGE_KEYS.PROGRESS) || '{}');
    return progress[`block${blockNumber}`] || null;
}

// Активация ключа
function activateKey(key) {
    const deviceID = getDeviceID();

    if (key && key.includes(deviceID)) {
        localStorage.setItem(STORAGE_KEYS.KEY, key);
        localStorage.setItem(STORAGE_KEYS.SUBSCRIPTION, 'paid');
        return true;
    }

    return false;
}
