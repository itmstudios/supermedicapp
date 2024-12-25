let WebApp = window.Telegram.WebApp;
let BackButton = WebApp.BackButton;
BackButton.show();

BackButton.onClick(function() {
    window.location.href = '/';
    BackButton.hide();
});