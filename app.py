from flask import Flask, render_template, flash, redirect, url_for, request
import psycopg2
from psycopg2 import sql, OperationalError
import sys
import configparser
from pathlib import Path

app = Flask(__name__)
app.secret_key = ''

# Функция для загрузки конфигурации
def load_db_config():
    config = configparser.ConfigParser()
    config_file = Path(__file__).parent / 'config.ini'
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    config.read(config_file)
    
    return {
        'host': config['database']['host'],
        'database': config['database']['database'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'port': config['database']['port']
    }

# Загружаем конфигурацию БД
try:
    DB_CONFIG = load_db_config()
except Exception as e:
    print(f"❌ Error loading database config: {e}")
    sys.exit(1)

COLUMN_NAMES = {
    'customers': {
        'customer_id': 'ID клиента',
        'full_name': 'ФИО',
        'passport_number': 'Паспорт',
        'date_of_birth': 'Дата рождения',
        'phone': 'Телефон',
        'email': 'Email',
        'address': 'Адрес'
    },
    'deposit_transactions': {
        'transaction_id': 'ID операции',
        'deposit_id': 'ID вклада',
        'transaction_date': 'Дата операции',
        'transaction_type': 'Тип операции',
        'amount': 'Сумма'
    },
    'deposit_types': {
        'deposit_type_id': 'ID типа',
        'name': 'Название вклада',
        'interest_rate': 'Процентная ставка',
        'minimum_amount': 'Минимальная сумма',
        'term_months': 'Срок (мес)',
        'is_replenishable': 'Пополняемый',
        'is_withdrawable': 'С возможностью снятия'
    },
    'deposits': {
        'deposit_id': 'ID вклада',
        'customer_id': 'ID клиента',
        'deposite_type_id': 'Тип вклада',
        'amount': 'Сумма',
        'open_date': 'Дата открытия',
        'close_date': 'Дата закрытия',
        'status': 'Статус'
    },
    'interest_accruals': {
        'accrual_id': 'ID начисления',
        'deposit_id': 'ID вклада',
        'accrual_date': 'Дата начисления',
        'interest_amount': 'Сумма процентов'
    },
    'users': {
        'customer_id': 'ID клиента',
        'first_name': 'Имя',
        'second_name': 'Фамилия',
        'passport_number': 'Паспорт',
        'phone': 'Телефон',
        'email': 'Email',
        'address': 'Адрес'
    }
}

def check_db_connection():
    """Проверяет соединение с базой данных"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        return True
    except OperationalError as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}", file=sys.stderr)
        return False

# Проверка подключения при старте приложения
with app.app_context():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Подключение к PostgreSQL успешно!")
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def get_table_data(table_name):
    """Получает данные из указанной таблицы с переведенными названиями колонок"""
    if not check_db_connection():
        raise OperationalError("Нет соединения с базой данных")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cursor.execute(query)
        
        # Получаем оригинальные названия столбцов
        original_columns = [desc[0] for desc in cursor.description]
        
        # Заменяем названия на русские
        display_columns = [COLUMN_NAMES.get(table_name, {}).get(col, col) 
                         for col in original_columns]
        
        # Получаем данные
        data = cursor.fetchall()
        
        return display_columns, data, original_columns
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/customers')
def list_customers():
    """Страница с клиентами"""
    try:
        columns, data, _ = get_table_data('customers')
        return render_template('table_template.html', 
                            title='Клиенты',
                            columns=columns, 
                            data=data)
    except OperationalError as e:
        flash(str(e), 'danger')
        return render_template('table_template.html', 
                            title='Клиенты',
                            columns=[], 
                            data=[])
    except Exception as e:
        flash(f'Произошла ошибка: {str(e)}', 'danger')
        return render_template('table_template.html', 
                            title='Клиенты',
                            columns=[], 
                            data=[])

@app.route('/deposit_transactions')
def list_transactions():
    """Страница с транзакциями"""
    try:
        columns, data, _ = get_table_data('deposit_transactions')
        return render_template('table_template.html', 
                            title='Операции по вкладам',
                            columns=columns, 
                            data=data)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'danger')
        return render_template('table_template.html', 
                            title='Операции по вкладам',
                            columns=[], 
                            data=[])

@app.route('/deposit_types')
def list_deposit_types():
    """Страница с типами вкладов"""
    try:
        columns, data, _ = get_table_data('deposit_types')
        return render_template('table_template.html', 
                            title='Типы вкладов',
                            columns=columns, 
                            data=data)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'danger')
        return render_template('table_template.html', 
                            title='Типы вкладов',
                            columns=[], 
                            data=[])

@app.route('/deposits')
def list_deposits():
    """Страница с вкладами"""
    try:
        columns, data, _ = get_table_data('deposits')
        return render_template('table_template.html', 
                            title='Вклады',
                            columns=columns, 
                            data=data)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'danger')
        return render_template('table_template.html', 
                            title='Вклады',
                            columns=[], 
                            data=[])

@app.route('/interest_accruals')
def list_interest_accruals():
    """Страница с начислениями процентов"""
    try:
        columns, data, _ = get_table_data('interest_accruals')
        return render_template('table_template.html', 
                            title='Начисления процентов',
                            columns=columns, 
                            data=data)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'danger')
        return render_template('table_template.html', 
                            title='Начисления процентов',
                            columns=[], 
                            data=[])

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    """Добавление нового пользователя"""
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Получаем данные из формы
            first_name = request.form['first_name']
            second_name = request.form['second_name']
            passport_number = request.form['passport_number']
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            
            # Вставляем нового пользователя
            query = """
                INSERT INTO users (first_name, second_name, passport_number, phone, email, address)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING customer_id
            """
            cursor.execute(query, (first_name, second_name, passport_number, phone, email, address))
            conn.commit()
            
            flash('Пользователь успешно добавлен!', 'success')
            return redirect(url_for('list_users'))
            
        except Exception as e:
            conn.rollback()
            flash(f'Ошибка при добавлении пользователя: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('add_user.html')

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Редактирование пользователя"""
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Получаем данные из формы
            first_name = request.form['first_name']
            second_name = request.form['second_name']
            passport_number = request.form['passport_number']
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            
            # Обновляем пользователя
            query = """
                UPDATE users 
                SET first_name = %s, second_name = %s, passport_number = %s, 
                    phone = %s, email = %s, address = %s
                WHERE customer_id = %s
            """
            cursor.execute(query, (first_name, second_name, passport_number, phone, email, address, user_id))
            conn.commit()
            
            flash('Данные пользователя успешно обновлены!', 'success')
            return redirect(url_for('list_users'))
            
        except Exception as e:
            conn.rollback()
            flash(f'Ошибка при обновлении пользователя: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    # Получаем данные пользователя для формы
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE customer_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('list_users'))
        
        # Получаем названия колонок
        columns = [desc[0] for desc in cursor.description]
        user_data = dict(zip(columns, user))
        
        return render_template('edit_user.html', user=user_data)
        
    except Exception as e:
        flash(f'Ошибка при получении данных пользователя: {str(e)}', 'danger')
        return redirect(url_for('list_users'))
    finally:
        cursor.close()
        conn.close()

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Удаление пользователя"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = "DELETE FROM users WHERE customer_id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        
        flash('Пользователь успешно удален!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при удалении пользователя: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    """Страница с пользователями с кнопками действий"""
    try:
        columns, data, _ = get_table_data('users')
        return render_template('table_template.html', 
                            title='Пользователи',
                            columns=columns + ['Действия'], 
                            data=data,
                            show_actions=True,
                            show_add_button=True,
                            add_url=url_for('add_user'),
                            add_button_text='Добавить пользователя')
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'danger')
        return render_template('table_template.html', 
                            title='Пользователи',
                            columns=[], 
                            data=[])

if __name__ == '__main__':
    app.run(debug=True)