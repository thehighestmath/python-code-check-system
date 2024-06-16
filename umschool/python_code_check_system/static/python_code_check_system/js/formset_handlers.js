$(document).ready(function() {
    $('#add-more').click(function(e) {
        e.preventDefault();
        let formIndex = $('#id_test_set-TOTAL_FORMS').val(); // Получаем начальный индекс форм
        console.log(formIndex)
        let testForm = $('.test-form:first').clone(true); // Клонирование первой формы
        testForm.find(':input').each(function() {
            let baseName = $(this).attr('name').replace(/-\d+-/, '-0-'); // получаем базовое имя с индексом 0
            let newName = baseName.replace('-0-', '-' + formIndex + '-');
            $(this).attr({
                'id': newName,
                'name': newName
            }).val(''); // очистка значений для новой формы
        });
        testForm.insertAfter($('.test-form:last')); // Вставка новой формы после последней

        $('#id_test_set-TOTAL_FORMS').val(parseInt(formIndex) + 1); // Обновляем значение общего количества форм
        formIndex++;
    });
});
