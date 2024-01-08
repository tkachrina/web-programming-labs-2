from flask import Blueprint, render_template, request, redirect, session
from Db import db
from Db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user


lab6 = Blueprint("lab6", __name__)

@lab6.route("/lab6/check")
def main():
    my_users = users.query.all()
    print(my_users)
    return "result in console!"


@lab6.route("/lab6/checkarticles")
def mainart():
    my_articles = articles.query.all()
    for article in my_articles:
        print(f"{article.title}-{article.article_text}")
    return "Result in console!"


@lab6.route('/lab6/menu')
def lab6_menu():
    username_form = session.get('username')
    return render_template('menu6.html', username = username_form)


@lab6.route("/lab6/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register6.html")
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    isUserExist = users.query.filter_by(username = username_form).first()

    errors = []

    if isUserExist is not None:
        errors.append("Такой пользователь уже существует!")
        return render_template("register6.html", errors = errors)
    elif not username_form:
        errors.append("Введите имя пользователя!")
        return render_template("register6.html", errors=errors)
    elif len(password_form) < 5:
        errors.append("Пароль должен содержать не менее 5 символов!")
        return render_template("register6.html", errors=errors)
    
    pw_hash = generate_password_hash(password_form)

    newUser = users(username = username_form, password = pw_hash)

    db.session.add(newUser)

    db.session.commit()

    return redirect("/lab6/login")

@lab6.route("/lab6/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login6.html")
    
    errors = []
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    my_user = users.query.filter_by(username = username_form).first()
    print(check_password_hash(my_user.password, password_form))

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect("/lab6/articles")

    if not (username_form or password_form):
        errors.append("Введите имя пользователя и пароль!")
        return render_template("login6.html", errors = errors)
    elif my_user is None:
        errors.append("Такого пользователя не существует! Зарегестрируйтесь!")
        return render_template("login6.html", errors = errors)
    elif my_user is not check_password_hash(my_user.password, password_form):
        errors.append("Введите правильный пароль!")
        return render_template("login6.html", errors = errors)
    elif my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect("/lab6/articles")
    
    return render_template("login6.html")


@lab6.route('/lab6/articles', methods = ['GET', 'POST'])
@login_required
def view_articles():
    username_form = request.form.get('username')
    my_articles = articles.query.filter((articles.user_id == current_user.id) | (articles.is_public == True)).order_by(articles.is_favorite.desc()).all()
    print(my_articles)
    return render_template('articles6.html', articles=my_articles, username_form = username_form)


@lab6.route("/lab6/newarticle", methods=["GET", "POST"])
@login_required
def createArticle():
    if request.method == "GET":
        return render_template("new_article6.html")
    article_text = request.form.get("article_text")
    title = request.form.get("article_title")
    if len(article_text) == 0:
        errors = ["Заполните текст"]
        return render_template("new_article6.html", errors=errors)
    new_article = articles(user_id=current_user.id, title=title, article_text=article_text)
        
    db.session.add(new_article)
    db.session.commit()
    
    return redirect("/lab6/articles")


@lab6.route("/lab6/articles/<int:article_id>", methods=['GET', 'POST'])
def getArticle(article_id):
    if current_user.is_authenticated:
        if request.method == 'POST':
            article = articles.query.filter_by(id=article_id).first()
        article = articles.query.filter_by(id=article_id).first()
        if article:
            if article.user_id == current_user.id or article.is_public:
                text = article.article_text.splitlines()
                return render_template("articlescheck6.html", article_text=text, article_title=article.title, username=current_user.username)


@lab6.route('/lab6/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab6/menu')