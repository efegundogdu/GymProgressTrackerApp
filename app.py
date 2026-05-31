from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
from functions import calculate_volume
app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        user = cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["user_id"] = user["id"]   
            return redirect(url_for("home"))
        else:
            return "Hatalı giriş"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        (username, password))
            conn.commit()
        except:
            return "This user already exists!"

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)

def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

def init_db():
    conn = get_connection()
    # Users tablosu zaten vardı
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    # Egzersiz Tablosu [cite: 27, 28, 29]
    conn.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        exercise_name TEXT NOT NULL,
        weight REAL,
        reps INTEGER,
        sets INTEGER,
        volume REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    conn.commit()
    conn.close()

    from functions import calculate_volume

@app.route("/add", methods=["POST"])
def add_exercise():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Formdan gelen veriler
    name = request.form.get("exercise_name")
    weight = float(request.form.get("weight"))
    reps = int(request.form.get("reps"))
    sets = int(request.form.get("sets"))
    
    # Business Logic kullanımı [cite: 42]
    vol = calculate_volume(weight, reps, sets)
    
    # Raw SQL kullanımı [cite: 26, 44]
    conn = get_connection()
    conn.execute("""
        INSERT INTO exercises (user_id, exercise_name, weight, reps, sets, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session["user_id"], name, weight, reps, sets, vol))
    conn.commit()
    conn.close()
    
    return redirect(url_for("home"))