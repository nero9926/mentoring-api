# mentoring

API для сервиса по наставничеству

### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке

- Cоздать и активировать виртуальное окружение: \
  `python -m venv venv` \
  `source venv/scripts/activate` \
  `python -m pip install --upgrade pip`

- Установить зависимости из файла requirements.txt: \
  `pip install -r requirements.txt`

- Выполнить миграции: \
  `python manage.py migrate` \
  `python manage.py makemigrations`

- Запустить проект: \
  `python manage.py runserver`

### API:

- `api/registration` - регистрация.
- `api/login` - авторизация.
- `api/users/` - список всех пользователей.
- `api/users/<id>` - информация о конкретном пользователе.
- `api/logout` - выход.
- `api/swagger/` - документация

Аутентификация реализована через djangorestframework-simplejwt с заголовком 'Bearer'
