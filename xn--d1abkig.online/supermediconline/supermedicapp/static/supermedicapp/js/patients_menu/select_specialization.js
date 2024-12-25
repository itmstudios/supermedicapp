document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    BackButton.show();
    BackButton.onClick(function() {
        window.location.href = `/select_specialist/`;
        BackButton.hide();
    });
    const specializationButtons = document.querySelectorAll("[data-specialization-id]");
    const specializationForm = document.getElementById("select-specialization");
    specializationButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const specializationId = button.getAttribute("data-specialization-id");
            specializationForm.action = `/select_specialist/${specializationId}/`;
            specializationForm.submit();
        });
    });
});