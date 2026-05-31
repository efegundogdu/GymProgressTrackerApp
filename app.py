from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
from functions import calculate_volume # Hacim hesabı fonksiyonun

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    # Tablo yapısını kodla tam uyumlu hali
    conn.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        weight REAL,
        reps INTEGER,
        sets INTEGER,
        volume REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    # Kullanıcı ismini ve antrenman listesini çekiyoruz
    user = conn.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    exercises = conn.execute("SELECT * FROM exercises WHERE user_id = ?", (session["user_id"],)).fetchall()
    conn.close()
    
    return render_template("index.html", exercises=exercises, username=user['username'])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]   
            return redirect(url_for("dashboard"))
        else:
            return "Hatalı giriş! <a href='/login'>Geri dön</a>"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            conn.close()
            return "Bu kullanıcı zaten var! <a href='/register'>Geri dön</a>"
    return render_template("register.html")

@app.route("/add_exercise", methods=["POST"])
def add_exercise():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Form Verileri
    try:
        name = request.form["name"]
        weight = float(request.form["weight"])
        reps = int(request.form["reps"])
        sets = int(request.form["sets"]) 
        user_id = session["user_id"]

        # Hacim hesabı
        vol = calculate_volume(weight, reps, sets)

        conn = get_connection()
        conn.execute("INSERT INTO exercises (user_id, name, weight, reps, sets, volume) VALUES (?, ?, ?, ?, ?, ?)", 
                     (user_id, name, weight, reps, sets, vol))
        conn.commit()
        conn.close()
    except Exception as e:
        return f"Bir hata oluştu: {e}"
    
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:id>")
def delete_exercise(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    conn.execute("DELETE FROM exercises WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)