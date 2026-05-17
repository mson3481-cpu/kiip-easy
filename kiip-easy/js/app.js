// Главный файл приложения

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});

// Инициализация приложения
function initApp() {
    console.log('KIIP Easy запущен');
    checkDeviceID();
}

// Проверка/генерация DeviceID
function checkDeviceID() {
    let deviceID = localStorage.getItem('kiip_user_id');

    if (!deviceID) {
        // Генерируем новый DeviceID
        const randomPart = Math.random().toString(36).substring(2, 7).toUpperCase();
        deviceID = 'Kiip_' + randomPart;
        localStorage.setItem('kiip_user_id', deviceID);
        console.log('Сгенерирован новый DeviceID:', deviceID);
    } else {
        console.log('DeviceID существует:', deviceID);
    }

    return deviceID;
}

// Открытие блока
function openBlock(blockNumber) {
    console.log('Открываем блок:', blockNumber);

    // TODO: проверить подписку для блоков 2-4
    // Пока все блоки ведут на заглушки

    switch(blockNumber) {
        case 1:
            window.location.href = 'pages/test-question.html?block=1';
            break;
        case 2:
            window.location.href = 'pages/test-question.html?block=2';
            break;
        case 3:
            window.location.href = 'pages/test-question.html?block=3';
            break;
        case 4:
            window.location.href = 'pages/test-question.html?block=4';
            break;
        default:
            console.error('Неизвестный блок:', blockNumber);
    }
}
