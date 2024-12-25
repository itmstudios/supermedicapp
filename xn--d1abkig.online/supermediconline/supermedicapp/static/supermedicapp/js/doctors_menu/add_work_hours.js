let WebApp = window.Telegram.WebApp;
let BackButton = WebApp.BackButton;
let MainButton = WebApp.MainButton;
MainButton.setText("ОТПРАВИТЬ");
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

function* hourGenerator(startHour, endHour) {
    for (let i = startHour; i <= endHour; i++) {
        yield i;
    }
}

function* minuteGenerator(step) {
    for (let i = 0; i < 60; i += step) {
        yield i;
    }
}

function addDateTime() {
    const dateTimeDiv = document.getElementById("new_work_hours");

    const dateTimeContainer = document.createElement("new_work_hours");
    dateTimeContainer.classList.add("form-group");

    const hourSelect = document.createElement("select");
    hourSelect.name = "hours";
    hourSelect.classList.add("select-option-doc");
    const hourOptionPlaceholder = document.createElement("option");
    hourOptionPlaceholder.value = "";
    hourOptionPlaceholder.disabled = true;
    hourOptionPlaceholder.selected = true;
    hourOptionPlaceholder.textContent = "Часы";
    hourSelect.appendChild(hourOptionPlaceholder);

    const hours = hourGenerator(7, 22);
    for (const hour of hours) {
        const option = document.createElement("option");
        option.value = hour;
        option.textContent = hour;
        hourSelect.appendChild(option);
    }

    const minuteSelect = document.createElement("select");
    minuteSelect.name = "minutes";
    minuteSelect.classList.add("select-option-doc");
    const minuteOptionPlaceholder = document.createElement("option");
    minuteOptionPlaceholder.value = "";
    minuteOptionPlaceholder.disabled = true;
    minuteOptionPlaceholder.selected = true;
    minuteOptionPlaceholder.textContent = "Минуты";
    minuteSelect.appendChild(minuteOptionPlaceholder);

    const minutes = minuteGenerator(5);
    for (const minute of minutes) {
        const option = document.createElement("option");
        option.value = minute;
        option.textContent = minute.toString().padStart(2, "0");
        minuteSelect.appendChild(option);
    }

    dateTimeContainer.appendChild(hourSelect);
    dateTimeContainer.appendChild(minuteSelect);

    dateTimeDiv.appendChild(dateTimeContainer);

    MainButton.show();
    $("#delete-date-time-block").show();
}

function removeDateTime() {
    const dateTimesDiv = document.getElementById("new_work_hours");
    const dateTimeContainers = dateTimesDiv.getElementsByTagName("new_work_hours");

    if (dateTimeContainers.length > 0) {
        dateTimesDiv.removeChild(dateTimeContainers[dateTimeContainers.length - 1]);
    }
    if (dateTimeContainers.length < 1) {
        $("#delete-date-time-block").hide();
    }
}

function checkDateTimeSelection() {
    const selectedHours = $("select[name='hours']").map(function() {
        return $(this).val();
    }).get();

    const selectedMinutes = $("select[name='minutes']").map(function() {
        return $(this).val();
    }).get();

    if (selectedHours.length === 0 || selectedHours.length !== selectedMinutes.length) {
        return false;
    }

    return true;
}

const dateTimeForm = document.getElementById("dateTimeForm");

MainButton.onClick(function() {
    if (!checkDateTimeSelection()) {
        WebApp.showAlert(`Пожалуйста, выберите все данные.`);
        return;
    } else {
        const formData = new FormData(dateTimeForm);
        $.ajax({
            url: `/success_change_time/${telegram_id}/${appointment_date}/`,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
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
        MainButton.hide();
    }
});


const tempButton = document.getElementById("temp-btn");
tempButton.addEventListener("click", function (event) {
    event.preventDefault();
    if (!checkDateTimeSelection()) {
        WebApp.showAlert(`Пожалуйста, выберите все данные.`);
        return;
    } else {
        const formData = new FormData(dateTimeForm);
        /*for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]);
        }*/
        $.ajax({
            url: `/success_change_time/${telegram_id}/${appointment_date}/`,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
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
        MainButton.hide();
    }
});
