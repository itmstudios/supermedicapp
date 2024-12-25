let WebApp = window.Telegram.WebApp;
let BackButton = WebApp.BackButton;
let MainButton = WebApp.MainButton;
MainButton.hide();

let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

const container = document.querySelector('.container');
let telegram_id = container.getAttribute('data-telegram-id');
let appointment_date = container.getAttribute('data-appointment-date');

BackButton.show();
BackButton.onClick(function() {
    var url = `/time_preview/${telegram_id}/${appointment_date}/`;
    window.location.href = url;
    BackButton.hide();
});

let selectedAppointments = [];

$(".time-checkbox").change(function() {
    let appointmentId = $(this).data("appointment-id");
    let isChecked = $(this).prop("checked");

    if (isChecked) {
        selectedAppointments.push(appointmentId);
    } else {
        let index = selectedAppointments.indexOf(appointmentId);
        if (index !== -1) {
            selectedAppointments.splice(index, 1);
        }
    }
    if (selectedAppointments.length > 0) {
        MainButton.setText("УДАЛИТЬ");
        MainButton.show();
    } else {
        MainButton.hide();
    }
});

MainButton.onClick(function() {
    if (selectedAppointments.length > 0) {
        $.ajax({
            url: `/success_delete/`,
            type: 'POST',
            data: {
                'appointments': selectedAppointments.toString(),
            },
            success: function(response) {
                if (!response.result) {
                    WebApp.showAlert(`Произошла ошибка. Повторите попытку.`);
                    console.log('false')
                } else {
                    WebApp.showAlert(`Расписание успешно обновлено.`);
                    console.log('success')
                };
            window.location.href = `/doctors/`;
            }
        });
    }
});

const tempButton = document.getElementById("temp-btn");
tempButton.addEventListener("click", function (event) {
    event.preventDefault();
    if (selectedAppointments.length > 0) {
        $.ajax({
            url: `/success_delete/`,
            type: 'POST',
            data: {
                'appointments': selectedAppointments.toString(),
            },
            success: function(response) {
                if (!response.result) {
                    WebApp.showAlert(`Произошла ошибка. Повторите попытку.`);
                    console.log('false')
                } else {
                    WebApp.showAlert(`Расписание успешно обновлено.`);
                    console.log('success')
                };
            window.location.href = `/doctors/`;
            }
        });
    }
});
