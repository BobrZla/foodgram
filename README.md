# Recipe Sharing Website

Это веб-приложение, позволяющее пользователям делиться своими рецептами, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.. Сайт работает в контейнере Docker, используя Nginx в качестве веб-сервера, Gunicorn в качестве WSGI-сервера и Python для бэкенд-разработки.

# Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

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


## Ресурсы запросов API  
- Ресурс <span style="color: #7FFFD4">**auth**</span>: аутентификация.
- Ресурс <span style="color: #7FFFD4">**users**</span>: пользователи.
- Ресурс <span style="color: #7FFFD4">**recipes**</span>: рецепты пользователей.
- Ресурс <span style="color: #7FFFD4">**tags**</span>: Теги для рецептов, например Завтрак,Обед, Полдник и т.д., новые теги добавляет админ.
- Ресурс <span style="color: #7FFFD4">**shopping_cart**</span>: Список покупок пользователей.
- Ресурс <span style="color: #7FFFD4">**favorite**</span>: Избранные рецепты пользователей.
- Ресурс <span style="color: #7FFFD4">**subscriptions**</span>: Подписки пользователей.  
- Ресурс <span style="color: #7FFFD4">**ingredients**</span>: Ингредиенты используемые в рецептах.
> Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.  
(файл Redoc.html)

## Примеры запросов API  
![Static Badge](https://img.shields.io/badge/POST_запрос-rgb(24,111,175))  
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Ответ JSON:  
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "text": "string",
  "cooking_time": 1
}
```
![Static Badge](https://img.shields.io/badge/GET_запрос-rgb(47,129,50))  
`http://example/api/tags/`  
Ответ JSON:  

```
[
  {
    "id": 0,
    "name": "Завтрак",
    "slug": "breakfast"
  }
]
```
![Static Badge](https://img.shields.io/badge/PATCH_запрос-rgb(191,88,29))  
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Ответ JSON:  
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "text": "string",
  "cooking_time": 1
}
```
![Static Badge](https://img.shields.io/badge/DEL_запрос-rgb(204,51,51))  
`http://example/api/recipes/{id}/shopping_cart/`  
Response ![Static Badge](https://img.shields.io/badge/-204_Рецепт_успешно_удален_из_списка_покупок-rgb(47,129,50))  

Автор backend'а:  
[Ярмишко Дмитрий](https://github.com/BobrZla) (c) 2024


