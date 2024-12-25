let csrfToken = getCookie('csrftoken');
setupAjax(csrfToken);

let tg = window.Telegram.Webapp;

//let user_name = 'nina';
//let telegram_username = 'tklkf';
//let telegram_id = 140787015;
let user_name = JSON.parse(new URLSearchParams(window.Telegram.WebApp.initData).get('user')).first_name;
let telegram_username = JSON.parse(new URLSearchParams(window.Telegram.WebApp.initData).get('user')).username;
let telegram_id = JSON.parse(new URLSearchParams(window.Telegram.WebApp.initData).get('user')).id;

$.ajax({
    url: '/save_tg_id/',
    type: 'POST',
    data: {
        'name':  user_name,
        'telegram_username':  telegram_username,
        'telegram_id':  telegram_id,
    },
});
