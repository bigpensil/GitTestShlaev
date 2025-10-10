from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
@app.route('/admin/')
def admin_panel():
    connection = sqlite3.connect('C:/Users/пользователь/Desktop/HH/testdatabase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM orders')
    products = cursor.fetchall()
    connection.close()
    print("products")
    return render_template("admin.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)