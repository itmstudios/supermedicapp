let WebApp = window.Telegram.WebApp;
let BackButton = WebApp.BackButton;
const container = document.querySelector('.container');
let telegram_id = container.getAttribute('data-telegram-id');
let appointment_date = container.getAttribute('data-appointment-date');

BackButton.show();
BackButton.onClick(function() {
    var url = `/update_work_time/${telegram_id}/`;
    window.location.href = url;
    BackButton.hide();
});

const addBtn = document.getElementById("add-btn");
const addForm = document.getElementById("add-work-hours-form");
addBtn.addEventListener("click", function (event) {
    event.preventDefault();
    addForm.action = `/add_work_hours/${telegram_id}/${appointment_date}/`;
    addForm.submit();
});

const deleteBtn = document.getElementById("delete-btn");
const deleteForm = document.getElementById("delete-work-hours-form");
deleteBtn.addEventListener("click", function (event) {
    event.preventDefault();
    deleteForm.action = `/delete_work_hours/${telegram_id}/${appointment_date}/`;
    deleteForm.submit();
});


