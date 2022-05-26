#  Foodgram - продуктовый помощник
![workflow](https://github.com/pro100cemuk/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)
[![Practicum.Yandex](https://img.shields.io/badge/-Practicum.Yandex-464646?style=flat&logo=Practicum.Yandex&logoColor=56C0C0&color=008080)](https://practicum.yandex.ru/)
## Описание
Сервис для публикации рецептов, подписок на публикации других пользователей, возможность добавлять рецепты в список «Избранное», а для приготовления блюд из рецептов для похода в магазин возможно скачивать сводный список продуктов из рецепта блюда.

## Описание Workflow
##### Workflow состоит из четырёх шагов:
###### tests
- Проверка кода на соответствие PEP8.
###### Push Docker image to Docker Hub
- Сборка и публикация образа на DockerHub.
###### deploy 
- Автоматический деплой на боевой сервер при пуше в главную ветку.
###### send_massage
- Отправка уведомления в телеграм-чат.

## Подготовка и запуск проекта
##### Клонирование репозитория
Склонируйте репозиторий на локальную машину:
```bash
git clone https://github.com/pro100cemuk/foodgram-project-react.git
```

## Установка на удаленном сервере (Ubuntu):
##### Шаг 1. Выполните вход на свой удаленный сервер
Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:
```bash
ssh <USERNAME>@<IP_ADDRESS>
```

##### Шаг 2. Установите docker на сервер:
Введите команду:
```bash
sudo apt install docker.io 
```

##### Шаг 3. Установите docker-compose на сервер:
Введите команды:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### Шаг 4. Локально отредактируйте файл nginx.conf
Локально отредактируйте файл `infra/nginx.conf` и в строке `server_name` впишите свой IP.

##### Шаг 5. Скопируйте подготовленные файлы из каталога infra:
Скопируйте подготовленные файлы `infra/docker-compose.yml` и `infra/nginx.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yml` и `home/<ваш_username>/nginx.conf` соответственно.
Введите команду из корневой папки проекта:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

##### Шаг 6. Cоздайте .env файл:
На сервере создайте файл `nano .env` и заполните переменные окружения (или создайте этот файл локально и скопируйте файл по аналогии с предыдущим шагом):
```bash
SECRET_KEY=<SECRET_KEY>
DEBUG=<True/False>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

##### Шаг 7. Добавьте Secrets:
Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

##### Шаг 8. После успешного деплоя:
Зайдите на боевой сервер и выполните команды:

###### На сервере соберите docker-compose:
```bash
sudo docker-compose up -d --build
```

###### Создаем и применяем миграции:
```bash
sudo docker-compose exec backend python manage.py makemigrations --noinput
sudo docker-compose exec backend python manage.py migrate --noinput
```
###### Подгружаем статику
```bash
sudo docker-compose exec backend python manage.py collectstatic --noinput 
```
###### Заполнить базу данных:
```bash
sudo docker-compose exec backend python manage.py load_data
```
###### Создать суперпользователя Django:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

##### Шаг 9. Проект запущен:
Проект будет доступен по вашему IP-адресу.

##### Open Source License
GPL v3 (can check in gpl-3.0.md file)

##### Автор
Семенов Евгений aka pro100cemuk 

##### Развёрнутый проект
http://51.250.67.180/
