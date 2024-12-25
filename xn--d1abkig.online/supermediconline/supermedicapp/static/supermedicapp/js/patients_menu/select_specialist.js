let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

let MainButton = WebApp.MainButton;
WebApp.expand();

MainButton.setText("ПРОДОЛЖИТЬ");
MainButton.hide();

MainButton.onClick(function() {
    window.location.href = '/get_user_info/';
    MainButton.hide();
});

document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.container');

    var specializationId = container.getAttribute('data-specialization-id');
    var doctorId = container.getAttribute('data-doctor-id');
    var appointmentDate = container.getAttribute('data-appointment-date');
    var appointmentTime = container.getAttribute('data-appointment-time');

    const selectSpecializationBtn = document.getElementById("select-specialization-btn");

    if (selectSpecializationBtn.textContent.trim() != "Выберите специализацию") {
        $('#doctor-block').show();
    } else {
        $('#doctor-block').hide();
        $('#select-date-block').hide();
        $('#time-block').hide();
        MainButton.hide();
    }

    const selectDoctorBtn = document.getElementById("select-doctor-btn");
    const doctorForm = document.getElementById("doctor-block");

    selectDoctorBtn.addEventListener("click", function (event) {
        event.preventDefault();
        if (specializationId) {
            doctorForm.action = `/select_doctor/${specializationId}/`;
            doctorForm.submit();
        }
    });

    if (selectDoctorBtn.textContent.trim() != "Выберите врача") {
        $('#select-date-block').show();
    } else {
        $('#select-date-block').hide();
        $('#time-block').hide();
        MainButton.hide();
    }

    const selectDateBtn = document.getElementById("select-date-btn");
    const dateForm = document.getElementById("select-date-block");

    selectDateBtn.addEventListener("click", function (event) {
        event.preventDefault();
        if (doctorId) {
            dateForm.action = `/select_date/${specializationId}/${doctorId}/`;
            dateForm.submit();
        }
    });

    if (selectDateBtn.textContent.trim() != "Выберите дату") {
        $('#time-block').show();
    } else {
        $('#time-block').hide();
        MainButton.hide();
    }

    const selectTimeBtn = document.getElementById("select-time-btn");
    const timeForm = document.getElementById("time-block");

    selectTimeBtn.addEventListener("click", function (event) {
        event.preventDefault();

        if (appointmentDate) {
            timeForm.action = `/select_time/${specializationId}/${doctorId}/${appointmentDate}/`;

            timeForm.submit();
        }
    });

    if (selectTimeBtn.textContent.trim() != "Выберите время") {
        MainButton.show();
       $('#appointment-btn').show();
    } else {
        MainButton.hide();
       $('#appointment-btn').hide();
    }
});

