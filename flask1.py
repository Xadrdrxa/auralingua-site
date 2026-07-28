from flask import Flask, render_template, request
import sqlite3

from flask_mail import Mail, Message


app = Flask(__name__)


# ---------------- EMAIL CONFIGURATION ----------------

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'auralin12ua@gmail.com'
app.config['MAIL_PASSWORD'] = 'zddb bbcr bwzh xcct'

mail = Mail(app)


# ---------------- DATABASE CREATION ----------------

def create_database():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            level TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    return render_template("index.html")


# ---------------- FORM SUBMISSION ----------------

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    level = request.form["level"]
    message = request.form["message"]


    # Save to database

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, email, phone, level, message)
        VALUES (?, ?, ?, ?, ?)
    """,
    (name, email, phone, level, message))


    conn.commit()
    conn.close()



    # Send email to teacher

    msg = Message(
        "New AuraLingua Student Inquiry",
        sender="auralin12ua@gmail.com",
        recipients=["auralin12ua@gmail.com"]
    )


    msg.body = f"""
New student inquiry:

Name:
{name}

Email:
{email}

Phone:
{phone}

German Level:
{level}

Message:
{message}
"""


    mail.send(msg)


    return "Thank you! We will contact you soon."



# ---------------- STUDENT DASHBOARD ----------------

@app.route("/students")
def students():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()


    return render_template(
        "students.html",
        students=data
    )



# ---------------- START SERVER ----------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )