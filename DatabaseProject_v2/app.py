from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # regex
        username_regex = re.compile(r'^[a-zA-Z0-9_]{5,15}$')
        password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,20}$')  

        if not username_regex.match(username):
            flash("Invalid username. Username must be 5-15 characters long and can contain alphanumeric characters and underscores only.")
            return redirect(url_for('register'))
        if not password_regex.match(password):
            flash("Password must be 8-20 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        ''')

        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            flash("Username already exists.")
            return redirect(url_for('register'))

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Failed to register user due to error: {e}")
            return redirect(url_for('register'))
        finally:
            conn.close()
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()  

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
            flash("Logged in successfully!") 
            return redirect(url_for('index'))  
        else:
            flash("Invalid username or password.")  
            return redirect(url_for('login'))  

    return render_template('login.html')

@app.route('/get_exercises', methods=['POST'])
def get_exercises():
    difficulty = request.form['difficulty']
    muscle_group = request.form['muscle_group']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT exercise FROM exercises WHERE difficulty = ? AND muscle_group = ?
    ''', (difficulty, muscle_group))
    exercises = cursor.fetchall()
    conn.close()

    modified_exercises = [{'exercise': exercise[0].replace('_', ' ')} for exercise in exercises]
    
    return render_template('index.html', exercises=modified_exercises)
    
@app.route('/add_to_program', methods=['POST'])
def add_to_program():
    exercise = request.form['exercise']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personal_program (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT
    )
    ''')
    cursor.execute('''
    INSERT INTO personal_program (exercise) VALUES (?)
    ''', (exercise,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('personal_program'))

@app.route('/personal_program')
def personal_program():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT exercise FROM personal_program')
    personal_exercises = cursor.fetchall()
    conn.close()
    
    return render_template('personal_program.html', personal_exercises=personal_exercises)

@app.route('/clear_program', methods=['POST'])
def clear_program():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM personal_program')
    conn.commit()
    conn.close()
    
    return redirect(url_for('personal_program'))

@app.route('/add_new_exercise', methods=['GET', 'POST'])
def add_new_exercise():
    if request.method == 'POST':
        exercise = request.form['exercise']
        difficulty = request.form['difficulty']
        muscle_group = request.form['muscle_group']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO exercises (exercise, difficulty, muscle_group) VALUES (?, ?, ?)
        ''', (exercise, difficulty, muscle_group))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('add_new_exercise.html')

if __name__ == '__main__':
    app.run(debug=True)
