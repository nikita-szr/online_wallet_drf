# 🪙 Online Wallet DRF

Online Wallet - это REST API сервис для управления онлайн-кошельком, созданный с использованием Django, Django REST Framework и Docker.

---

##  Стек технологий

- **Python 3.12**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL**
- **Docker & Docker Compose**

---

##  Установка и запуск

### Клонирование репозитория

```bash
https://github.com/nikita-szr/online_wallet_drf/tree/feature_1
cd online_wallet_drf
```
### Запуск
```bash
Создайте файл .env на основе шаблона .env.sample:
```
```bash
Создайте и активируйте виртуальное окружение на основании файла requirements.txt
```

```bash
Запустите проект командой 'python manage.py runserver'
```

##  Запуск Docker

```bash
docker-compose up --build -d

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```
