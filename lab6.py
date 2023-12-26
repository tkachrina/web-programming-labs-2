from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, Blueprint, session
import psycopg2
from Db import db
from Db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab6 = Blueprint("lab6", __name__)


@lab6.route("/lab6/check")
def main():
    # тоже самое, что select * from users;
    my_users = users.query.all()
    print(my_users)
    return "result in console!"

@lab6.route("/lab6/checkarticles")
def mainart():
    my_articles = articles.query.all()
    for article in my_articles:
        print(f"{article.title}-{article.article_text}")
    return "Result in console!"

@lab6.route('/lab6/register', methods=['GET', 'POST'])
def register():
    errors = []
    numLab = '6'

    if request.method=='GET':
        return render_template('register.html', numLab=numLab)
    
    username_form=request.form.get('username')
    password_form=request.form.get('password')

    '''
    Проверяем существование пользователя в БД с таким же именем
    Если такого нет, то в isUserExist вернется None
    т.е. мы можем интерпретировать это как False
    ''' 

    ''' 
    select * from users
    WHERE username = username_form
    LIMIT  1
    --где username_form - это имя, которое мы получили из формы
    ''' 
    isUserExists=users.query.filter_by(username=username_form).first()

    if isUserExists is not None:
        errors.append("Пользователь с данным именем уже существует")
        return render_template('register.html', errors=errors, numLab=numLab)
    elif not username_form:
        errors.append("Введите имя пользователя")
        return render_template("register.html", errors=errors, numLab=numLab)
    elif len(password_form) < 5:
        errors.append("Пароль должен содержать не менее 5 символов")
        return render_template("register.html", errors=errors, numLab=numLab)
    
    # хэшируем пароль
    hashedPswd=generate_password_hash(password_form, method='pbkdf2')
    # создаем объект users с нужными полями
    newUser=users(username=username_form, password=hashedPswd)

    # это INSERT
    db.session.add(newUser)
    # Тоже самое, что и conn.commit()
    db.session.commit()

    return redirect('/lab6/login')





@lab6.route("/lab6/login", methods=["GET", "POST"])
def login():
    errors = []
    numLab = '6'

    if request.method == "GET":
        return render_template("login.html", numLab=numLab)
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    my_user = users.query.filter_by(username = username_form).first()

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            # сохраняем JWT токен
            login_user(my_user, remember=False)
            return redirect("/lab6")

    if not (username_form or password_form):
        errors.append("Пожалуйста заполните все поля")
        return render_template("login.html", errors = errors, numLab=numLab)
    elif my_user is None:
        errors.append("Такого пользователя не существует")
        return render_template("login.html", errors = errors, numLab=numLab)
    elif my_user is not check_password_hash(my_user.password, password_form):
        errors.append("Введите правильный пароль")
        return render_template("login.html", errors = errors, numLab=numLab)

    
    return render_template("login.html", numLab=numLab)




# login_required - авторизация обязательна,
# если пользователь не авторизован, то перенаправить
# на страницу lab6/login (lab6/login мы указывали в app.py)

# функцию login_required и переменную current_user
# мы импортировали ранее из Flask-Login
@lab6.route('/lab6/articles')
@login_required
def view_article():
    numLab = '6'
    # select * from articles where user_id = current_user.id
    my_articles = articles.query.filter_by(user_id=current_user.id)
    my_articles = my_articles.order_by(articles.is_favorite.desc()).all()
    return render_template('view_article.html', articles=my_articles, numLab=numLab)





@lab6.route("/lab6/articles/<int:article_id>", methods=["GET", "POST"])
@login_required
def getArticle(article_id):
    numLab = '6'

    # select * from articles where user_id = current_user.id
    my_articles = articles.query.filter_by(id=article_id).first()
    
    if my_articles is None:
        return "Not found!"

    text = my_articles.article_text.splitlines()

    return render_template('articleN.html', article_text=text, article_title=my_articles.title, 
                            numLab=numLab, is_favorite=my_articles.is_favorite, article_id=my_articles.id)


@lab6.route('/lab6/articles/<int:article_id>/publish', methods=['POST'])
def publish_article(article_id):
    my_articles = articles.query.filter_by(id=article_id).first()
    if request.form.get("is_public") == 'True':
            is_public_form = True
            my_articles.is_public = is_public_form
            db.session.commit()
    return redirect(f"/lab6/articles/{article_id}")


@lab6.route('/lab6/articles/<int:article_id>/favorite', methods=['POST'])
def favorite_article(article_id):
    my_articles = articles.query.filter_by(id=article_id).first()
    if request.form.get("is_favorite") == 'True':
            is_favorite_form = True
            my_articles.is_favorite = is_favorite_form
            db.session.commit()
    elif request.form.get("is_favorite") == 'False':
        is_favorite_form = False
        my_articles.is_favorite = is_favorite_form
        db.session.commit()
    return redirect(f"/lab6/articles/{article_id}")


@lab6.route('/lab6/articles/<int:article_id>/likes', methods=['POST'])
def like_article(article_id):
    my_articles = articles.query.filter_by(id=article_id).first()

    if not my_articles:
        return "Not found!"

    if my_articles.likes is None:
        my_articles.likes = 0
    my_articles.likes += 1
    return redirect(f"/lab6")




@lab6.route("/lab6/new_article", methods=['GET','POST'])
@login_required
def createArticle():
    numLab = '6'
    errors = ''
    if request.method == "GET":
        return render_template("new_article.html", numLab=numLab)

    if request.method == "POST":
        text_article = request.form.get("text_article")
        title = request.form.get("title_article")

        if len(text_article) == 0:
            errors = 'Заполните текст'
            return render_template("new_article.html", errors=errors, numLab=numLab)

    new_article = articles(user_id=current_user.id, title=title, article_text=text_article, 
                            is_public=False)
    
    db.session.add(new_article)
    db.session.commit()

    return redirect(f"/lab6/articles/{new_article.id}")





@lab6.route("/lab6")
def main6lab():
    if current_user is not None and current_user.is_authenticated:
        visibleUser = current_user.username
        public_articles = db.session.query(
                        articles.title,
                        articles.article_text,
                        users.username,
                        ).join(users, articles.user_id == users.id,
                        ).filter(articles.is_public == True, articles.user_id == current_user.id
                        ).order_by(articles.is_favorite.desc())
    else:
        visibleUser = 'Anon'
        public_articles = db.session.query(articles.title, 
                        articles.article_text, 
                        users.username
                        ).join(users, articles.user_id == users.id
                        ).filter(articles.is_public == True)
    

    return render_template("lab6.html", username = visibleUser, public_articles=public_articles)



@lab6.route("/lab6/logout")
@login_required
def logout():
    logout_user()
    return redirect('/lab6')