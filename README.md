# Recipe Sharing Website

Это веб-приложение, позволяющее пользователям делиться своими рецептами. Сайт работает в контейнере Docker, используя Nginx в качестве веб-сервера, Gunicorn в качестве WSGI-сервера и Python для бэкенд-разработки.

## Установка и запуск приложения
1. Склонируйте репозиторий:  
   git clone git@github.com:BobrZla/foodgram.git
2. Залейте его себе на github  
3. Создайте в корне проекта файл  .env  
Внутри которого заполните такие данные:
```python
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
# Добавляем переменные для Django-проекта:
DB_HOST=db
DB_PORT=5432
SECRET_KEY=Ваш джанго ключ
DEBUG=True/False в зависимости от режима в котором хотите запустить
ALLOWED_HOSTS=ip вашего сервера,127.0.0.1,localhost,ваш сайт
```
4. В настройках  github actions - secrets  
заполните следующие данные:  

```python
DOCKER_PASSWORD - логин с докерхаба
DOCKER_USERNAME - пароль с докерхаба
HOST - айпи адрес вашего сервера
SSH_KEY - приватный ключ от сервера
SSH_PASSPHRASE - "пароль от сервера"
USER - имя пользователя на сервере
```

5. Пушим проект на сервер и радуемся

## Стек технологий:
- Django==3.2.3  
- djangorestframework==3.12.4
- djoser==2.1.0
- django-extra-fields==3.0.2
- psycopg2-binary==2.9.9
- django-filter==22.1
- python-dotenv==1.0.1
- gunicorn==20.1.0
- Pillow==9.0.0