$(document).ready(function() {
    let csrfToken = getCookie('csrftoken');
    setupAjax(csrfToken);
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    let MainButton = WebApp.MainButton;
    MainButton.setText("ВНЕСТИ ПРЕДОПЛАТУ И ЗАПИСАТЬСЯ");
    MainButton.show();

    let container = document.querySelector('.container');
    let specializationId, doctorId, appointmentDate, appointmentTime, appointmentId;
    if (container) {
        appointmentId = container.getAttribute('data-appointment-id');
        specializationId = container.getAttribute('data-specialization-id');
        doctorId = container.getAttribute('data-doctor-id');
        appointmentDate = container.getAttribute('data-appointment-date');
        appointmentTime = container.getAttribute('data-appointment-time');
    }
    BackButton.show();
    BackButton.onClick(function() {
        if (specializationId && doctorId && appointmentDate && appointmentTime && appointmentId) {
            window.location.href = `/select_specialist/${specializationId}/${doctorId}/${appointmentDate}/${appointmentTime}/${appointmentId}/`;
            BackButton.hide();
        }
    });

    MainButton.onClick(function() {
        let lastName = $('#last-name').val();
        let firstName = $('#first-name').val();
        let middleName = $('#middle-name').val();
        let phoneNumber = $('#phone-number').val();
//        let telegram_username = 'talkinghead5';
        let telegram_username = JSON.parse(new URLSearchParams(window.Telegram.WebApp.initData).get('user')).username;
        let telegram_id = JSON.parse(new URLSearchParams(window.Telegram.WebApp.initData).get('user')).id;
        let phoneRegex = /^\+\d{10,12}$/;

        if (!lastName || !firstName || !phoneNumber) {
            WebApp.showAlert(`Пожалуйста, заполните все поля.`);
        };

        if (!phoneRegex.test(phoneNumber)) {
            WebApp.showAlert(`Введите номер телефона в формате +12345678900`);
        } else {
            $.ajax({
                url: '/submit_appointment/',
                type: 'POST',
                data: {
                    'user_last_name': lastName,
                    'user_first_name': firstName,
                    'user_middle_name': middleName,
                    'user_phone_number': phoneNumber,
                    'user_telegram_username': telegram_username,
                    'user_telegram_id': telegram_id,
                },
                success: function(response) {
                    if (!response.result) {
                        WebApp.showAlert(`Произошла ошибка. Повторите попытку, выбрав другое время.`);
                    } else {
                        WebApp.showAlert(`Заявка успешно оформлена. Скоро бот пришлет Вам ссылку на оплату.`);
                    };

                WebApp.close();
                }
            });
        };
    });

    $('#next-btn').click(function (event) {
        event.preventDefault();
        let lastName = $('#last-name').val();
        let firstName = $('#first-name').val();
        let middleName = $('#middle-name').val();
        let phoneNumber = $('#phone-number').val();
        let telegram_username = 'talkinghead5';

        if (!lastName || !firstName || !phoneNumber) {
            WebApp.showAlert(`Пожалуйста, заполните все поля.`);
        } else {
            $.ajax({
                url: '/submit_appointment/',
                type: 'POST',
                data: {
                    'user_last_name': lastName,
                    'user_first_name': firstName,
                    'user_middle_name': middleName,
                    'user_phone_number': phoneNumber,
                    'user_telegram_username': telegram_username,
                },
                success: function(response) {
                    if (!response.result) {
                        WebApp.showAlert(`Произошла ошибка. Повторите попытку, выбрав другое время.`);
                    } else {
                        WebApp.showAlert(`Заявка успешно оформлена. Скоро бот пришлет Вам ссылку на оплату.`);
                    };
                    WebApp.close();
                }
            });
        };
    });
});

