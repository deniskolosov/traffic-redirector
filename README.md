# traffic-redirector
Система редиректа пользователей на лендинг страницы с использованием коротких ссылок.

Для запуска:
```
export TDS_HOSTNAME=<ваше_имя_хоста в формате хост:порт>
source ./venv/bin/activate
python manage.py migrate
python manage.py runserver
```