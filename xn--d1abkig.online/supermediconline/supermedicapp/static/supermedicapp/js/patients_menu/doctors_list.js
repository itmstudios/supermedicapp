let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    let container = document.querySelector('.container');
    let specialization_id;
    specialization_id = container.getAttribute('data-specialization-id');
    BackButton.show();
    BackButton.onClick(function() {
        if (specialization_id) {
            window.location.href = `/select_specialist/${specialization_id}/`;
            BackButton.hide();
        }
    });
    const doctorButtons = document.querySelectorAll("[data-doctor-id]");
    const doctorForm = document.getElementById("doctor-form");
    doctorButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const specializationId = button.getAttribute("data-specialization-id");
            const doctorId = button.getAttribute("data-doctor-id");
            if (doctorId) {
                doctorForm.action = `/doctors_info/${specializationId}/${doctorId}/`;
                doctorForm.submit();
            }
        });
    });
});

