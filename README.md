# API для проекта YaMDb

Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**:
- «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники». 
- «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. 

Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

# Технологии:

- Django 3.2
- Проект написан на Python 3.8 с использованием веб-фреймворка Django REST Framework.
- Библиотека Simple JWT - работа с JWT-токеном
- База данных - SQLite3

# Как запустить проект в dev-режиме:

**Клонировать репозиторий** `api_yamdb` **и перейти в него в командной строке:**
```PYTHON
	git clone git@github.com:hatecodinglovemoney/api_yamdb.git
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

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт [http://127.0.0.1:8000/api/v1/auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/). 
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

## Ссылка на полную докуметацию (ReDoc) для API для проекта YaMDb - [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

# Импорт CSV файлов в БД:
1. Желательно проводить импорт в чистую БД.
2. Запустить команду в терминале: 
```BASH
  Linux:~$ python3 manage.py import_csv
  Win, Mac:~$ python manage.py import_csv
```
3. Ожидать полной отработки скрипта

# Авторы:
[**Ната Бутрина**](https://github.com/hatecodinglovemoney)

[**Соболев Кирилл**](https://github.com/sblvkr)

[**Лев Андреев**](https://github.com/LevAndreevS)
