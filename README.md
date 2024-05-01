
# Foodgram

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

___
«Продуктовый помощник»: сайт, где пользователи могут публиковать собственные рецепты, добавлять чужие рецепты в избранное, подписываться на публикации других авторов. Список покупок позволяет пользователям создавать список продуктов, необходимых для приготовления выбранных блюд, и скачать его перед походом в магазин.
___


### Технологии

Python 3.7, Django 2.2, DRF, Docker, Docker-compose, Djoser, NGINX, PostgreSQL, Gunicorn, Yandex.Cloud


### Шаблон наполнения env-файла
Файл должен располагаться в директории foodgram-project-react/infra 
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_penguinw
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<your-key-should-be-here>
```


### Последовательность действий для запуска проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке.
```
git clone https://github.com/madpenguinw/foodgram-project-react
```

- Из корневой директории перейти в папку infra
```
cd infra/
```

- Запустить контейнеры с проектом
```
docker-compose up -d
```

- Выполнить миграции
```
docker-compose exec backend python manage.py migrate
```

- Создать суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```

- Собрать статику
```
docker-compose exec backend python manage.py collectstatic --no-input
```

- Сделать дамп базы данных
```
docker-compose exec backend python manage.py dumpdata > fixtures.json
```

- Теперь доступна админ панель http://localhost/admin/
Документация на  http://localhost/api/docs/. Основной сайт доступен по адресу http://localhost/

- Для завершения работы необходимо остановить контейнеры
```
docker-compose stop
```

---

### Автор

Челноков Евгений
