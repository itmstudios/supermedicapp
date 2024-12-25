let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

document.addEventListener("DOMContentLoaded", function () {
    let WebApp = window.Telegram.WebApp;
    WebApp.expand();
    let BackButton = WebApp.BackButton;

    const daysTag = document.querySelector(".days"),
    currentDate = document.querySelector(".current-date"),
    prevNextIcon = document.querySelectorAll(".icons span");

    let date = new Date(),
    currYear = date.getFullYear(),
    currMonth = date.getMonth();

    const months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
                  "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];

    function isLeapYear(year) {
        return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    }

    const container = document.querySelector('.wrapper');

    let specializationId = container.getAttribute('data-specialization-id');
    let doctorId = container.getAttribute('data-doctor-id');

    BackButton.show();
    BackButton.onClick(function() {
        if (specializationId && doctorId) {
            var url = `/select_specialist/${specializationId}/${doctorId}/`;
            window.location.href = url;
            BackButton.hide();
        }
    });

    function fetchAppointmentDates() {
        $.ajax({
            url: '/get_appointment_dates/',
            type: 'POST',
            data: {
                'specialization_id': specializationId,
                'doctor_id': doctorId
            },
            success: function(response) {
                renderCalendar(response)
            },
        });
    }

    const renderCalendar = (appointmentDates = []) => {
        let firstDayofMonth = new Date(currYear, currMonth, 1).getUTCDay(),
            lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(),
            lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getUTCDay(),
            lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate();

        if (currMonth === 1 && isLeapYear(currYear)) {
            lastDateofMonth = 29;
        }

        let liTag = "";

        for (let i = firstDayofMonth; i > 0; i--) {
            liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
        }

        for (let i = 1; i <= lastDateofMonth; i++) {
            let isBackendDate = appointmentDates.includes(
                `${currYear}-${String(currMonth + 1).padStart(2, "0")}-${String(i).padStart(2, "0")}`
            )
            ? "active"
            : "";

            const isToday =
                i === date.getDate() &&
                currMonth === date.getMonth() &&
                currYear === date.getFullYear();

            if (isToday) {
                if (appointmentDates.includes(
                    `${currYear}-${String(currMonth + 1).padStart(2, "0")}-${String(i).padStart(2, "0")}`
                )) {
                    liTag += `<li class="active today" style="color: #d3325b;">${i}</li>`;
                } else {
                    liTag += `<li class="today" style="color: #d3325b;">${i}</li>`;
                }
            } else {
                liTag += `<li class="${isBackendDate}">${i}</li>`;
            }
        }

        for (let i = lastDayofMonth; i < 6; i++) {
            liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`;
        }

        currentDate.innerText = `${months[currMonth]}`;
        daysTag.innerHTML = liTag;
    }

    fetchAppointmentDates();

    prevNextIcon.forEach(icon => {
        icon.addEventListener("click", () => {
            currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
            if(currMonth < 0 || currMonth > 11) {
                date = new Date(currYear, currMonth, new Date().getDate());
                currYear = date.getFullYear();
                currMonth = date.getMonth();
            } else {
                date = new Date();
            }
            fetchAppointmentDates();
        });
    });


//    function formatDate(date) {
//        const day = date.getDate().toString().padStart(2, '0');
//        const month = (date.getMonth() + 1).toString().padStart(2, '0');
//        const year = date.getFullYear().toString();
//
//        return `${day}.${month}.${year}`;
//    }

    function formatAppointmentDate(date) {
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear().toString();
        return `${year}-${month}-${day}`;
    }

    daysTag.addEventListener("click", (event) => {
        const clickedDate = event.target;
        if (clickedDate.classList.contains("active")) {
            let year = currYear;
            let month = currMonth + 1;
            let day = clickedDate.innerText;
//            const formattedDate = formatDate(new Date(year, month - 1, day));
            const appointmentDate = formatAppointmentDate(new Date(year, month - 1, day));
            window.location.href = `/select_specialist/${specializationId}/${doctorId}/${appointmentDate}/`;
        }
    });
    $('#calendar-body').show();
});
