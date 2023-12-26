from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, Blueprint, session
import psycopg2

lab5 = Blueprint("lab5", __name__)

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


@lab5.route("/lab5")
def main():
    visibleUser = session.get("username")
    if visibleUser is not None:  
        visibleUser = visibleUser
    else:
        visibleUser = 'Anon'

    # visibleUser = "Anon"
    # visibleUser = session.get("username")

    return render_template("lab5.html", username = visibleUser)

    # conn = dbConnect()
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM users;")

    # result = cur.fetchall()
    # print(result)
    # dbClose(cur, conn)

    # return "go to console"


@lab5.route("/lab5/users")
def users():
    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")

    result = cur.fetchall()

    print(result)

    dbClose(cur, conn)

    return render_template("users.html", result=result)


@lab5.route('/lab5/register', methods=["GET", "POST"])
def registerPage():
    errors = []
    numLab = '5'
    visibleUser = "Anon"
    visibleUser = session.get("username")
    # Если это метод GET, то верни шаблон и заверши выполнение 
    if request.method == "GET": 
        return render_template("register.html", errors=errors, username=visibleUser, numLab=numLab)

    # Если мы попали сюда, значит это метод РОЅT,
    # так как GЕT мы уже обработали и сделали return.
    # После return функция немедленно завершается 
    username = request.form.get("username") 
    password = request.form.get("password")

    # Провряем username и password на пустоту в 
    # Если любой из них пустой, то добавляем ошибку 
    # и рендерим шаблон
    if not (username or password): 
        errors.append("Пожалуйста, заполните все поля") 
        print(errors) 
        return render_template("register.html", errors=errors, username=visibleUser, numLab=numLab)
    
    # получаем пароль от пользователя, хэшируем его
    hashPassword = generate_password_hash(password)
    # Если мы попали сюда, значит username и password заполненны
    # Подключаемся к БД
    conn = dbConnect()
    cur = conn.cursor()

    # Проверяем наличие клиента в базе
    # У нас не может быть два пользователя с одинаковыми логинами

    # WARNING: мы используем f-строки, что не рекомендуется делать 
    # позже мы разберемся с Вами почему не стоит так делать
    cur.execute(f"SELECT username FROM users WHERE username = %s;", (username,))

    # fetchone, a отличие, от fetchall, получает только одну строку 
    # мы задали свойство UNIQUE для пользователя, значит
    # больше одной строки мы не можем получить
    # Только один пользователь с таким именем может быть в БД
    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")
       
        conn.close()
        cur.close()

        return render_template("register.html", errors=errors, username=visibleUser, numLab=numLab)

    # Если мы попали сюда, то значит в cur.fetchone нет ни одной строки
    # значит пользователя с таким же логином не существует
    cur.execute(f"INSERT INTO users (username, password) VALUES (%s,%s);", (username, hashPassword)) 
    # сохраняем пароль в виде хэша в БД
    
    
    # делаем commit - т.е. фиксируем изменения
    conn.commit()
    conn.close()
    cur.close
    
    return redirect("/lab5/login")


@lab5.route('/lab5/login', methods=["GET", "POST"])
def loginPage():
    errors = []
    numLab = '5'

    if request.method == "GET":
        return render_template("login.html", errors=errors, numLab=numLab)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста заполните все поля")
        return render_template("login.html", errors=errors, numLab=numLab)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))

    result = cur.fetchone()

    if result is None:
        errors.append("Неправильный логин или пароль")
        dbClose(cur, conn)
        return render_template("login.html", errors=errors, numLab=numLab)

    userID, hashPassword = result

    # с помощью check_password_hash сравниваем хеш и 
    # пароль из БД. Функция "check_password_hash"
    # сама переведет password  в хэш
    if check_password_hash(hashPassword, password):
        # пароль правильный

        # сохраняем id и username
        # в сессию (JWT токен)
        session['id'] = userID
        session['username'] = username
        dbClose(cur, conn)
        return redirect("/lab5")

    else:
        errors.append("Неправильный логин или пароль")
        return render_template("login.html", errors=errors, numLab=numLab)


@lab5.route('/lab5/new_article', methods=['GET', 'POST'])
def createArticle():
    errors = []
    numLab = '5'
    visibleUser = "Anon"
    visibleUser = session.get("username")

    # проверян авторизован ли пользователь
    # Мы читаем из JWT токена (session.get) ID пользовтеля
    userID = session.get("id")

    if userID is not None:
        # пользовател авторизован, мы прочитали JWT токен
        # проверили его валидность. Получили его id
        if request.method=='GET':
            return render_template('new_article.html', username = visibleUser, numLab=numLab)
        
        if request.method=='POST':
            text_article = request.form.get("text_article")
            title = request.form.get("title_article")

            if len(text_article) == 0:
                errors.append("Заполните текст")
                return render_template('new_article.html', errors=errors, username = visibleUser, numLab=numLab)
            
            conn = dbConnect()
            cur = conn.cursor()

            cur.execute(f"INSERT INTO articles(user_id, title, articl_text) VALUES (%s, %s, %s) RETURNING id;", (userID, title, text_article))
            # получаем id от вновь созданной записи.
            # в нашем случае мы будем получать статьи след образом
            # /lab5/article/id_article
            new_article_id = cur.fetchone()[0]
            conn.commit()

            dbClose(cur,conn)

            # делаем редирект на новую статью
            # пока этот роут не сделан будет ошибка
            # чтобы получить статью под №5, необходимо
            # ввести в роут /lab5/articles/5
            return redirect(f"/lab5/articles/{new_article_id}")
        
    # пользователь не авторизован, отправить на стр логина
    return redirect ("/lab5/login")
    

# конструкция /<string:article_id> позволяет нам
# получить это значение в роуте 
# параметр к функции getArticle, как показано ниже

# например, если /lab5/articles/123
# то article_id = '123'
@lab5.route("/lab5/articles/<int:article_id>")
def getArticle(article_id):
    numLab = '5'
    userID = session.get("id")
    username = "Anon"

    # проверяем авторизован ли пользователь
    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute(f"SELECT title, articl_text FROM articles WHERE id = %s and user_id = %s;", (article_id, userID))

        # возьми одну строку
        articleBody = cur.fetchone()

        dbClose(cur, conn)
       
        if articleBody is None:
            return "Not found!"
        
        # разбиваем строку на массив по "Enter", чтобы
        # с помощью цикла for в jinja разбить статью на параграфы
        text = articleBody[1].splitlines()

        return render_template("articleN.html", article_text=text, numLab=numLab, 
article_title=articleBody[0], username=session.get("username"))


@lab5.route("/lab5/view_article")
def view_article():
    numLab = '5'
    userID = session.get("id")
    username = "Anon"
    
    # проверяем авторизован ли пользователь
    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute("SELECT id, title FROM articles WHERE user_id = %s;", (userID,))

        # возьми одну строку
        articleList = cur.fetchall()

        if articleList is None:
            return "Not found!"

        articles = [{'id': row[0], 'title': row[1]} for row in articleList]

        dbClose(cur, conn)

        return render_template("view_article.html", articles=articles, 
                                username=session.get("username"), numLab=numLab)

    # Пользователь не авторизован
    return redirect("/lab5/login")


@lab5.route("/lab5/logout")
def logout():
    session.clear()
    return redirect('/lab5/login')