document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;
    const specializationButtons = document.querySelectorAll("[data-specialization-id]");
    const specializationForm = document.getElementById("select-specialization");
    specializationButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const specializationId = button.getAttribute("data-specialization-id");
            console.log(specializationId);
            specializationForm.action = `/our_doctors/${specializationId}/`;
            specializationForm.submit();
        });
    });
    BackButton.show();
    BackButton.onClick(function() {
        window.location.href = `/our_doctors/`;
        BackButton.hide();
    });
});