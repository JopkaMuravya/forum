document.addEventListener('DOMContentLoaded', function() {
    // Инициализируем Emoji Button
    const picker = new EmojiButton();

    // Находим иконку смайлика и текстовое поле "Описание"
    const emojiButton = document.querySelector('.icon-Emoticon');
    const descriptionField = document.querySelector('textarea[name="description"]');

    // Открываем панель выбора смайликов при нажатии на иконку
    emojiButton.addEventListener('click', function() {
        picker.togglePicker(emojiButton);
    });

    // Добавляем выбранный смайлик в текстовое поле "Описание"
    picker.on('emoji', function(emoji) {
        descriptionField.value += emoji;
    });
});
