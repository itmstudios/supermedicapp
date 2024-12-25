`git clone <repo>`

`cd xn--d1abkig.online/supermediconline`

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`

В этом репозитории содержится только веб-сайт, созданный для использования внутри телеграм бота.

Чтобы добавить это приложение в бота, необходимо разместить сайт на удаленном сервере с SSL, далее см. https://core.telegram.org/bots/webapps#launching-mini-apps-from-the-menu-button