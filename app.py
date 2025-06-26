from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os
from config import db_config

app = Flask(__name__)
app.secret_key = 'secret_key'

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/todo')
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect('/todo')
    return render_template('login.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        task = request.form['task']
        cursor.execute('INSERT INTO todos (user_id, task) VALUES (%s, %s)', (session['user_id'], task))
        conn.commit()
    cursor.execute('SELECT * FROM todos WHERE user_id = %s', (session['user_id'],))
    todos = cursor.fetchall()
    conn.close()
    return render_template('todo.html', todos=todos)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id=%s AND user_id=%s', (task_id, session['user_id']))
        conn.commit()
        conn.close()
    return redirect('/todo')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)




# from flask import Flask, render_template, request, redirect, session, url_for
# import mysql.connector
# from config import db_config

# app = Flask(__name__)
# app.secret_key = 'secret_key'

# def get_db_connection():
#     return mysql.connector.connect(**db_config)

# @app.route('/')
# def home():
#     if 'user_id' in session:
#         return redirect('/todo')
#     return redirect('/login')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
#         conn.commit()
#         conn.close()
#         return redirect('/login')
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
#         user = cursor.fetchone()
#         conn.close()
#         if user:
#             session['user_id'] = user['id']
#             return redirect('/todo')
#     return render_template('login.html')

# @app.route('/todo', methods=['GET', 'POST'])
# def todo():
#     if 'user_id' not in session:
#         return redirect('/login')
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     if request.method == 'POST':
#         task = request.form['task']
#         cursor.execute('INSERT INTO todos (user_id, task) VALUES (%s, %s)', (session['user_id'], task))
#         conn.commit()
#     cursor.execute('SELECT * FROM todos WHERE user_id = %s', (session['user_id'],))
#     todos = cursor.fetchall()
#     conn.close()
#     return render_template('todo.html', todos=todos)

# @app.route('/delete/<int:task_id>')
# def delete(task_id):
#     if 'user_id' in session:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('DELETE FROM todos WHERE id=%s AND user_id=%s', (task_id, session['user_id']))
#         conn.commit()
#         conn.close()
#     return redirect('/todo')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect('/login')

# if __name__ == '__main__':
#     app.run(debug=True)
