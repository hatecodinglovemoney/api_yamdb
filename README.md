# API для проекта YaMDb

Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**:
- «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники». 
- «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. 

Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

# Технологии:

- Проект написан на Python 3.8 с использованием веб-фреймворка Django REST Framework.
- Библиотека Simple JWT - работа с JWT-токеном
- База данных - SQLite3
-  requirements.txt:
```BASH
requests==2.26.0
Django==3.2
djangorestframework==3.12.4
django-filter==2.4.0
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
djangorestframework-simplejwt==5.2.2
```

# Как запустить проект в dev-режиме:

**Клонировать репозиторий** `api_yamdb` **и перейти в него в командной строке:**
```PYTHON
	cd api_yamdb
```
**Cоздать и активировать виртуальное окружение:**
```PYTHON
	Linux:~$ python3 -m venv venv
	Win, Mac:~$ python -m venv venv
```
```PYTHON
	source venv/bin/activate
```
**Установить зависимости из файла requirements.txt:**
```PYTHON
	Linux:~$ python3 -m pip install --upgrade pip
	Win, Mac:~$ python -m pip install --upgrade pip
```
```PYTHON
	Linux:~$ pip3 install -r requirements.txt	
	Win, Mac:~$ pip install -r requirements.txt
```
**Выполнить миграции:**
```PYTHON
	Linux:~$ python3 manage.py migrate
	Win, Mac:~$ python manage.py migrate
```
**Создайте суперпользователя:**
```PYTHON
	Linux:~$ python3 manage.py createsuperuser
	Win, Mac:~$ python manage.py createsuperuser
```
**Запустить проект:**
```PYTHON
	Linux:~$ python3 manage.py runserver
	Win, Mac:~$ python manage.py runserver
```

# Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладет правами администратора (`admin`)

# Алгоритм регистрации новых пользователей и получение JWT-токенов

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`. 
- **Доступно без токена**.
- **Использовать имя `me` в качестве `username` запрещено**. 
- **Поля `email` и `username` должны быть уникальными**.
```BASH
POST http://127.0.0.1:8000/api/v1/auth/signup/
```
```JSON
{
	"email": "user@example.com",
	"username": "string"
}
```

2. **YaMDB** отправляет письмо с кодом подтверждения `confirmation_code` на адрес `email`.
3. Пользователь коотправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
```JSON
{
  "username": "string",
  "confirmation_code": "string"
}
```

Ответ: `JWT-токен`

```JSON
{
  "token": "string"
}
```
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле

## Примеры:

# CATEGORIES (Категории произведений)

**Получение списка всех категорий:**
- **Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/categories/
```
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

**Создание новой категории:**
- **Права доступа: Администратор.**
- **Поле `slug` каждой категории должно быть уникальным.**

```BASH
POST http://127.0.0.1:8000/api/v1/categories/
```
```JSON
{
"name": "string",
"slug": "string"
}
```

**Удаление категории:**
- **Права доступа: Администратор.**

```BASH
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```

# GENRES (Категории жанров)

**Получение списка жанров:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/genres/
```
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

**Добавление жанра:**
- **Права доступа: Администратор.**
- **Поле `slug` каждого жанра должно быть уникальным.**

```BASH
POST http://127.0.0.1:8000/api/v1/genres/
```
```JSON
{
"name": "string",
"slug": "string"
}
```

**Удаление жанра:**
- **Права доступа: Администратор.**

```BASH
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```

# TITLES (Произведения)

**Получение списка всех произведений:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/titles/
```
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

**Добавление произведения:**
- **Права доступа: Администратор.**
- **Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).**
- **При добавлении нового произведения требуется указать уже существующие категорию и жанр.**

```BASH
POST http://127.0.0.1:8000/api/v1/titles/
```
```JSON
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

**Получение информации о произведении:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
```JSON
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

**Частичное обновление информации о произведении:**
- **Права доступа: Администратор.**

```BASH
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
```JSON
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

**Удаление произведения:**
- **Права доступа: Администратор.**

```BASH
DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

# REVIEWS (Отзывы)

**Получение списка всех отзывов:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

**Добавление нового отзыва:**
-  **Пользователь может оставить только один отзыв на произведение.**
-  **Права доступа: Аутентифицированные пользователи.**

```BASH
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```JSON
{
  "text": "string",
  "score": 1
}
```

**Полуение отзыва по `id`:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
```JSON
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**Частичное обновление отзыва по `id`:**
- **Права доступа: Автор отзыва, модератор или администратор.**

```BASH
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
```JSON
{
  "text": "string",
  "score": 1
}
```

**Удаление отзыва по `id`:**
- **Права доступа: Автор отзыва, модератор или администратор.**

```BASH
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

# COMMENTS (Комментарии к отзывам)

**Получение списка всех комментариев к отзыву:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

**Добавление комментария к отзыву:**
- **Права доступа: Аутентифицированные пользователи.**

```BASH
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```JSON
{
  "text": "string"
}
```


**Получение комментария к отзыву:**
- **Права доступа: Доступно без токена.**

```BASH
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
```JSON
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**Частичное обновление комментария к отзыву:**
- **Права доступа: Автор комментария, модератор или администратор.**

```BASH
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

```JSON
{
  "text": "string"
}
```

**Удаление комментария к отзыву:**
- **Права доступа: Автор комментария, модератор или администратор.**

```BASH
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

# USERS (Пользователи)

**Получение списка всех пользователей:**
- **Права доступа: Администратор.**

```BASH
GET http://127.0.0.1:8000/api/v1/users/
```
```JSON
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```

**Добавление пользователя:**
- **Права доступа: Администратор.**
- **Поля `email` и `username` должны быть уникальными.**

```BASH
POST http://127.0.0.1:8000/api/v1/users/
```
```JSON
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

**Получение пользователя по `username`:**
- **Права доступа: Администратор.**

```BASH
GET http://127.0.0.1:8000/api/v1/users/{username}/
```
```JSON
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

**Изменение данных пользователя по `username`:**
- **Права доступа: Администратор.**
- **Поля `email` и `username` должны быть уникальными.**

```BASH
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
```
```JSON
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

**Удаление пользователя по `username`:**
- **Права доступа: Администратор.**

```BASH
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
```

**Получение данных своей учетной записи:**
- **Права доступа: Любой авторизованный пользователь.**

```BASH
GET http://127.0.0.1:8000/api/v1/users/me/
```
```JSON
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

**Изменение данных своей учетной записи:**
- **Права доступа: Любой авторизованный пользователь.
- **Поля `email` и `username` должны быть уникальными.**

```BASH
PATCH http://127.0.0.1:8000/api/v1/users/me/
```
```JSON
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

# Авторы:
**Наталья Бутрина** -  https://github.com/hatecodinglovemoney

**Соболев Кирилл** - https://github.com/sblvkr

**Лев Андреев** - https://github.com/LevAndreevS
