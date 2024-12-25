document.addEventListener("DOMContentLoaded", function () {
    const appointmentsCarousel = document.getElementById("appointments-carousel");
    const appointmentsItems = document.querySelectorAll(".appointments-item");
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");
    let currentIndex = 0;

    function showCurrentAppointment() {
        appointmentsItems.forEach((item, index) => {
            if (index === currentIndex) {
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
        });
    }

    showCurrentAppointment();

    prevButton.addEventListener("click", function () {
        currentIndex = (currentIndex - 1 + appointmentsItems.length) % appointmentsItems.length;
        showCurrentAppointment();
    });

    nextButton.addEventListener("click", function () {
        currentIndex = (currentIndex + 1) % appointmentsItems.length;
        showCurrentAppointment();
    });
});
