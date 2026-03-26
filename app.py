from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id INTEGER,
        date TEXT,
        status TEXT,
        note TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def driver():
    conn = get_db()
    c = conn.cursor()
    drivers = c.execute("SELECT * FROM drivers").fetchall()

    if request.method == "POST":
        driver_id = request.form["driver"]
        date = request.form["date"]
        status = request.form["status"]

        c.execute("INSERT INTO availability (driver_id, date, status) VALUES (?, ?, ?)",
                  (driver_id, date, status))
        conn.commit()

    conn.close()
    return render_template("driver.html", drivers=drivers)

@app.route("/admin")
def admin():
    conn = get_db()
    c = conn.cursor()
    data = c.execute('''
        SELECT d.name, a.date, a.status, a.note
        FROM availability a
        JOIN drivers d ON d.id = a.driver_id
        ORDER BY a.date DESC
    ''').fetchall()
    conn.close()
    return render_template("admin.html", data=data)

@app.route("/add-driver", methods=["GET", "POST"])
def add_driver():
    if request.method == "POST":
        name = request.form["name"]
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO drivers (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect("/admin")
    return render_template("add_driver.html")

if __name__ == "__main__":
    app.run(debug=True)
