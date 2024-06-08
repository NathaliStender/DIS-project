import csv
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the exercises table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        difficulty TEXT,
        muscle_group TEXT
    )
    ''')

    # Create the users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Import exercises from a CSV file
    with open('Fitness.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')  
        next(reader)  # Skip the header
        for row in reader:
            cursor.execute('''
            INSERT INTO exercises (exercise, difficulty, muscle_group)
            VALUES (?, ?, ?)
            ''', (row[0], row[1], row[2]))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
