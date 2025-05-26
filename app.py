from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                (id INTEGER PRIMARY KEY,
                player TEXT,
                points INTEGER,
                rebounds INTEGER,
                assists INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['post'])
def submit():
    player = request.form['player']
    points = request.form['points']
    rebounds = request.form['rebounds']
    assists = request.form['assists']
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    c.execute("INSERT INTO stats (player, points, rebounds, assists) VALUES (?, ?, ?, ?)",
                (player, points, rebounds, assists))
    conn.commit()
    conn.close()
    return redirect('/stats')

@app.route('/stats')
def stats():
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    c.execute("SELECT id, player, points, rebounds, assists FROM stats")
    data = c.fetchall()
    conn.close()
    return render_template('stats.html', stats=data)

@app.route('/delete/<int:stat_id>', methods=['POST'])
def delete(stat_id):
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    c.execute("DELETE FROM stats WHERE id = ?", (stat_id,))
    conn.commit()
    conn.close()
    return redirect('/stats')

@app.route('/delete_all', methods=['POST'])
def delete_all():
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    c.execute("DELETE FROM stats")
    conn.commit()
    conn.close()
    return redirect('/stats')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)