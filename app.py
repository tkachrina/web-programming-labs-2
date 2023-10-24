from flask import Flask, redirect, url_for
app = Flask (__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)   

@app.route("/menu")
def menu():
      return """ 
<!doctype html>
<html>
    <head>
        <title> НГТУ, ФБ, Лабораторные работы </title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB- программирование, часть 2. Список лабораторных, меню 
        </header>

        <ol> 
            <li> 
                <a href="/lab1" target="_blank"> Лабораторная работа 1 </a> 
            </li> 
        </ol> 

        <h1>web-сервер на flask</h1>

        
        <a href="/lab1">Первая лабораторная работа</a>

        <footer style="margin-top:20px;">
            &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>   
"""      
@app.route("/lab1")
def lab1():
        return """
        <!doctype html>
        <html>
            <head>
                <title> Ткаченко Екатерина Игоревна, лабораторная 1 </title>
            </head>
            <body>
            <header>
                НГТУ, ФБ, Лабораторная работа 1
            </header>

            <h1>web-сервер на flask</h1>

            <p>
                Flask — фреймворк для создания веб-приложений на языке 
                программирования Python, использующий набор инструментов 
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так 
                называемых микрофреймворков — минималистичных каркасов 
                веб-приложений, сознательно предоставляющих лишь самые базовые возможности 
            </p>

            <a href="/menu" >Меню</a>
            
            <ol>
            <h2>Реализованные роуты</h2>
            </ol>
            
            <ol>
            <li><a href="/lab1/oak">Дуб</a></li>

            </ol>

            <footer style="margin-top:20px;">
                &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
            </footer>
            </body>
        </html>    
        """
@app.route("/lab1/oak/")
def oak ():
  return '''
    <!doctype html>
    <header>
      НГТУ, ФБ, WEB- программирование, часть 2.
    </header>
    <html>
      <body>
        <h1>Дуб</h1>
        <img src="''' + url_for('static', filename='oak.png') + '''">
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''" />
        <footer style="margin-top:20px;">
                &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
        </footer>
      </body>
    </html>
'''
