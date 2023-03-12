![workflow](https://github.com/atikhobaev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?)

### foodgram-project-react

# Дипломный проект курса "Бэкенд Разработчик" (Яндекс Практикум)

Server IP:  
[84.201.128.70](http://84.201.128.70/)  
[84.201.128.70/admin/](http://84.201.128.70/admin/)  
логин admin@admin.admin  
пароль s!e7SRRsZc%Vz8  

логины и пароли остальных пользователей [тут](https://github.com/atikhobaev/foodgram-project-react/blob/master/backend/data/users.csv)  

### Описание

Онлайн-сервис и API для него. На этом сервисе пользователи 
могут публиковать рецепты, подписываться на публикации других 
пользователей, добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

### Запуск проекта

Скопируйте проект на свой компьютер:

```
git clone https://github.com/atikhobaev/foodgram-project-react
```

Перейдите в директорию проекта:

```
cd backend
```

Cоздайте и активируйте виртуальное окружение для этого проекта:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создайте файл .env в директории backend и заполните его данными по этому 
образцу:

```
SECRET_KEY='some_secret_key'
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=False
```

Создайте образ backend (текущая директория должна быть backend):

```
docker build -t bazaz/foodgram_backend:latest .
```

Перейдите в директорию infra:

```
cd ../infra
```

Запустите docker compose:

```
docker compose up
```

Выполните миграции в контейнере созданном из образа backend:

```
docker compose exec -it backend python manage.py migrate
```

Загрузите статические файлы в контейнере созданном из образа backend:

```
docker compose exec -it backend python manage.py collectstatic --no-input
```

Для импорта приготовлены пользователи, ингридиенты, тэги и рецепты

```
docker compose exec -it backend python manage.py fill_users
```
  
```
docker compose exec -it backend python manage.py fill_ingredients
```
  
```
docker compose exec -it backend python manage.py fill_tags
```
  
```
docker compose exec -it backend python manage.py fill_recipes
```


Запустите проект в браузере.
Введите в адресную строку браузера:

```
localhost
```
  
Андрей Тихобаев  
https://github.com/atikhobaev  
https://t.me/atikhobaev