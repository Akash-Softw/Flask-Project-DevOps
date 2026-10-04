from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "data/tasks.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT id, title FROM tasks ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():

    task = request.form.get("task", "").strip()

    if task:
        conn = get_db_connection()

        conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (task,)
        )

        conn.commit()
        conn.close()

    return redirect("/")


@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/update/<int:id>", methods=["POST"])
def update_task(id):

    task = request.form.get("task", "").strip()

    if task:
        conn = get_db_connection()

        conn.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (task, id)
        )

        conn.commit()
        conn.close()

      

    return redirect("/")


@app.route("/about")
def about():
    return "This is my Flask Task Manager project where Jenkins and Docker is included "


@app.route("/health")
def health():
    return "Application is healthy"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
