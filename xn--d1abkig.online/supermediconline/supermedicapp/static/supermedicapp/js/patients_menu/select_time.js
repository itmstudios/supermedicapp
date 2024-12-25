let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    let container = document.querySelector('.container');
    let specialization_id, doctor_id, appointment_date;
    specialization_id = container.getAttribute('data-specialization-id');
    doctor_id = container.getAttribute('data-doctor-id');
    appointment_date = container.getAttribute('data-appointment-date');

    BackButton.show();
    BackButton.onClick(function() {
        if (specialization_id && doctor_id && appointment_date) {
            window.location.href = `/select_specialist/${specialization_id}/${doctor_id}/${appointment_date}/`;
            BackButton.hide();
        }
    });
    const timeButtons = document.querySelectorAll("[data-appointment-id]");
    const timeForm = document.getElementById("select-time");
    timeButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const appointmentId = button.getAttribute("data-appointment-id");
            const specializationId = button.getAttribute("data-specialization-id");
            const doctorId = button.getAttribute("data-doctor-id");
            const appointmentDate = button.getAttribute("data-appointment-date");
            const appointmentTime = button.getAttribute("data-appointment-time");
            timeForm.action = `/select_specialist/${specializationId}/${doctorId}/${appointmentDate}/${appointmentTime}/${appointmentId}/`;
            timeForm.submit();
        });
    });
});