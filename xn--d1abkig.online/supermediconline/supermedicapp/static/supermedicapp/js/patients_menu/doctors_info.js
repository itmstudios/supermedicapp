document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    let MainButton = WebApp.MainButton;
    MainButton.setText("ПРОДОЛЖИТЬ");
    MainButton.show();
    let container = document.querySelector('.container');
    let specializationId, doctorId;

    specializationId = container.getAttribute('data-specialization-id');
    doctorId = container.getAttribute('data-doctor-id');


    MainButton.onClick(function() {
        if (specializationId && doctorId) {
            var url = `/select_specialist/${specializationId}/${doctorId}/`;
            window.location.href = url;
            MainButton.hide();
        }
    });
    BackButton.show();
    BackButton.onClick(function() {
        if (specializationId) {
            window.location.href = `/select_doctor/${specializationId}/`;
            BackButton.hide();
        }
    });

    const tempButton = document.getElementById("temp-btn");
    tempButton.addEventListener("click", function (event) {
        event.preventDefault();
        var url = `/select_specialist/${specializationId}/${doctorId}/`;
        window.location.href = url;
    });
});
