let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    let container = document.querySelector('.container');
    const doctorButtons = document.querySelectorAll("[data-doctor-id]");
    const doctorForm = document.getElementById("doctor-form");
    doctorButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const specializationId = button.getAttribute("data-specialization-id");
            const doctorId = button.getAttribute("data-doctor-id");
            if (doctorId) {
                doctorForm.action = `/our_doctors_description/${doctorId}/`;
                doctorForm.submit();
            }
        });
    });
});