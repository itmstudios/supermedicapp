let WebApp = window.Telegram.WebApp;
let telegram_id = JSON.parse(new URLSearchParams(window.Telegram.WebApp.initData).get('user')).id;
//let telegram_id = 140787016;

const timeBtn = document.getElementById("update-work-time-btn");
const timeForm = document.getElementById("update-work-time");
timeBtn.addEventListener("click", function (event) {
    event.preventDefault();
    if (telegram_id) {
        timeForm.action = `/update_work_time/${telegram_id}/`;
        timeForm.submit();
    }
});

const myPatientBtn = document.getElementById("my-patients-btn");
const myPatientForm = document.getElementById("my-patients");
myPatientBtn.addEventListener("click", function (event) {
    event.preventDefault();
    if (telegram_id) {
        myPatientForm.action = `/my_patients/${telegram_id}/`;
        myPatientForm.submit();
    } else {
        WebApp.showAlert(`Кажется, Вы не врач. Если это ошибка, свяжитесь с администратором`);
        WebApp.close();
    }
});