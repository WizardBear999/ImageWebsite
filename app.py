import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Ensure the database and table exists
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gallery')
def gallery():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    images = c.fetchall()
    conn.close()
    return render_template('gallery.html', images=images)

@app.route('/add', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO images (title, url) VALUES (?, ?)", (title, url))
        conn.commit()
        conn.close()
        return redirect('/gallery')
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))  # required for Replit
    app.run(host='0.0.0.0', port=port)