# 🏦 Bank Deposit Management System

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-14+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Полнофункциональная система управления банковскими вкладами** с веб-интерфейсом

## ✨ Особенности

- 📊 Полный CRUD-функционал для клиентов, вкладов и транзакций
- 🔐 Ролевая модель доступа (администратор, оператор, клиент)
- 📈 Автоматический расчет процентов по вкладам
- 📱 Адаптивный интерфейс на Bootstrap 5
- 📁 Логирование всех операций

## 🛠 Технологии

**Backend:**
- Python 3.10+
- Flask 2.0+
- SQLAlchemy 1.4+
- Psycopg2 2.9+

**Frontend:**
- Bootstrap 5.1
- Jinja2
- Chart.js (визуализация)

**База данных:**
- PostgreSQL 14+

## 🚀 Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/wxxxenly/bank_site_practice
cd bank_site_practice

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить подключение (скопировать и отредактировать)
cp config.example.ini config.ini

# 4. Запустить приложение
flask run
