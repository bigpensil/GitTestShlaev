from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog/')
def catalog():
    connection = sqlite3.connect('C:/Users/пользователь/Desktop/HH/testdatabase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    connection.close()
    return render_template("catalog.html", cars=cars)

@app.route('/order/<int:car_id>', methods=['GET', 'POST'])
def order(car_id):
    connection = sqlite3.connect('C:/Users/пользователь/Desktop/HH/testdatabase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cars WHERE id = ?', (car_id,))
    car_data = cursor.fetchone()
    connection.close()
    
    if not car_data:
        return "Автомобиль не найден", 404
    
    car = {
        'id': car_data[0],
        'name': car_data[1],
        'price': car_data[2],
        'year': car_data[3],
        'image': car_data[4]
    }
    
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        comments = request.form.get('comments', '')
        
        # Здесь можно сохранить заказ в базу данных
        connection = sqlite3.connect('C:/Users/пользователь/Desktop/HH/testdatabase.db')
        cursor = connection.cursor()    
        
        # Создаем таблицу для заказов если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                car_name TEXT,
                customer_name TEXT,
                phone TEXT,
                email TEXT,
                comments TEXT,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Сохраняем заказ
        cursor.execute('''
            INSERT INTO orders (car_id, car_name, customer_name, phone, email, comments)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (car_id, car['name'], name, phone, email, comments))
        
        connection.commit()
        connection.close()
        
        # Показываем страницу успеха
        return render_template('order.html', 
                             car=car, 
                             success=True, 
                             customer_name=name, 
                             phone=phone)
    
    return render_template('order.html', car=car, success=False)

@app.route('/admin/')
def admin_panel():
    try:
        connection = sqlite3.connect('C:/Users/пользователь/Desktop/HH/testdatabase.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM orders')  
        products = cursor.fetchall()
        connection.close()
        print("Количество заказов:", len(products))
        return render_template("admin.html", products=products)
    except Exception as e:
        print(f"Ошибка: {e}")
        return f"Ошибка базы данных: {e}"
  
@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.route('/feedback/')
def feedback():
    return render_template('feedback.html')

@app.route('/company/')
def company():
    return render_template('company.html')

@app.route('/career/')
def career():
    return render_template('career.html')

if __name__ == "__main__":
    app.run(debug=True)