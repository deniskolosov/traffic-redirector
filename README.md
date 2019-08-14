# traffic-redirector
Система редиректа пользователей на лендинг страницы с использованием коротких ссылок.

Для запуска:
```
export TDS_HOSTNAME=<ваше_имя_хоста в формате хост:порт>
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
