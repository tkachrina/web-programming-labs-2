from flask import Blueprint, redirect, render_template, request, session, url_for
import psycopg2
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

lab5 = Blueprint('lab5', __name__)

def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="knowledge_base_for_ekaterina",
        user="ekaterina_knowledge_base", 
        password="123")
    return conn

def dbClose(cursor, connection):
    cursor.close()
    connection.close()


@lab5.route('/lab5/pages')
def lab():
    return render_template("pages.html")

@lab5.route("/lab5/")
def main():
    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("select * from users")

    result = cur.fetchall()

    print(result)

    dbClose(cur, conn)

    return redirect(url_for("lab5.menu"))

@lab5.route("/lab5/user")
def show_user():
    conn = dbConnect()
    cur = conn.cursor()

    cur = conn.cursor()

    cur.execute("SELECT username FROM users;")

    results = cur.fetchall()

    dbClose(cur, conn)

    return render_template('lab5.html', users=results)

@lab5.route('/lab5/menu')
def lab5_glav():
    username = session.get('user_name')
    return render_template('menu.html', username=username)


@lab5.route("/lab5/menu")
def menu():
    return render_template("menu.html")


@lab5.route('/lab5/register', methods=["GET", "POST"])
def registrPage():
    errors = []

    if request.method == "GET":
        return render_template('register.html', errors=errors)



    username = request.form.get("username")
    password = request.form.get("password")


    if not (username or password):
        errors.append("Пожалуйста заполните все поля")
        print(errors)
        return render_template('register.html', errors=errors)

    hashPassword = bcrypt.generate_password_hash(password).decode('utf-8')


    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE username = %s;", (username,))
    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")

        conn.close()
        cur.close()
        return render_template('register.html', errors=errors)

    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashPassword))

    conn.commit()
    conn.close()
    cur.close()

    return redirect("/lab5/login5")


@lab5.route('/lab5/login5', methods=["GET", "POST"])
def loginPage():
    errors = []
    
    if request.method == "GET":
        return render_template("login5.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста заполните все поля")
        return render_template("login5.html", errors=errors)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))

    result = cur.fetchone()

    if result is None:
        errors.append("Неправильный логин или пароль")
        dbClose(cur, conn)
        return render_template("login5.html", errors=errors)

    userID, hashPassword = result

    print(hashPassword)
    print(password)

    pw_hash = bcrypt.generate_password_hash(password, 10)
    hash = bcrypt.check_password_hash(pw_hash, password) # returns True

    if hash:
        session['id'] = userID
        session['user_name'] = username
        dbClose(cur, conn)
        return redirect("/lab5/menu")

    else:
        errors.append("Неправильный логин или пароль")
        return render_template("login5.html", errors=errors)


@lab5.route("/lab5/new_article", methods=["GET", "POST"])
def createArticle():
    errors = []

    userID = session.get('id')
    username = session.get('user_name')
    if userID is not None:
        if request.method =="GET":
            return render_template("new_article.html", username=username)

        if request.method == "POST":
            article_text = request.form.get("article_text")
            title = request.form.get("article_title")

            if article_text is None or len(article_text) == 0:
                errors.append("Заполните текст")
                return render_template("new_article", errors = errors, username=username)

            conn = dbConnect()
            cur = conn.cursor()

            cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s) RETURNING id;", (userID, title, article_text))


            new_articl_id = cur.fetchone()[0]
            conn.commit()

            dbClose(cur, conn)

            return redirect(f"/lab5/articles/{new_articl_id}")

    return redirect("/lab5/login5")


@lab5.route('/lab5/articles')
def list_articles():
    userID = session.get('id')
    username = session.get("user_name")

    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute("SELECT id, title FROM articles WHERE user_id = %s;", (userID,))
        articles_data = cur.fetchall()

        articles = [{'id': row[0], 'title': row[1]} for row in articles_data]

        dbClose(cur, conn)

        return render_template('articles.html', articles=articles, username=username)

    return redirect("/lab5/login5")


@lab5.route("/lab5/articles/<int:article_id>")
def getArticle(article_id):
    userID = session.get('id')
    username = session.get("user_name")

    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute("SELECT title, article_text FROM articles WHERE id = %s AND user_id = %s", (article_id, userID))

        articleBody = cur.fetchone()

        dbClose(cur, conn)

        if articleBody is None:
            return "Not found!", 404

        text = articleBody[1].splitlines()

    return render_template("articlescheck.html", article_text=text, article_title=articleBody[0], username = username)