from flask import Flask, redirect, url_for, render_template
app = Flask (__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)   

@app.route("/menu")
def menu():
      return ''' 
<!doctype html>
<html>
    <head>
        <title> НГТУ, ФБ, Лабораторные работы </title>
    </head>
    
    <header>
            НГТУ, ФБ, WEB- программирование, часть 2. Список лабораторных, меню 
        </header>

    <body>

        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''" />
        <h1>web-сервер на flask</h1>

        <ol> 
            <li> 
                <a href="/lab1" target="_blank"> Лабораторная работа 1 </a> 
            </li> 
            <li> 
                <a href="/lab2/example" target="_blank"> Лабораторная работа 2 </a> 
            </li> 
        </ol> 

        <footer style="margin-top:20px;">
            &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>   
'''     
@app.route("/lab1")
def lab1():
        return '''
        <!doctype html>
        <html>
            <head>
                <title> Ткаченко Екатерина Игоревна, лабораторная 1 </title>
            </head>
            <body>
            <header>
                НГТУ, ФБ, Лабораторная работа 1
            </header>

            <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''" />

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
            <li><a href="/lab1/student">Студентка НГТУ</a></li>
            <li><a href="/lab1/python">Язык программирования Python</a></li>
            <li><a href="/lab1/color">Воздействие цветов на мозг</a></li>

            </ol>

            <footer style="margin-top:20px;">
                &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
            </footer>
            </body>
        </html>    
        '''
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

@app.route("/lab1/student/")
def nstu ():
  return '''
    <!doctype html>
    <header>
      НГТУ, ФБ, WEB- программирование, часть 2.
    </header>
    <html>
      <body>
        <h1>Ткаченко Екатерина Игоревна</h1>
        <img src="''' + url_for('static', filename='nstu.png') + '''">
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''" />
        
        <footer style="margin-top:20px;">
                &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
        </footer>
      </body>
    </html>
'''

@app.route("/lab1/python/")
def  pytn():
  return '''
    <!doctype html>
    <header>
      НГТУ, ФБ, WEB- программирование, часть 2.
    </header>
    <html>
      <body>
        <h1>Язык программирования Python</h1>
        <p>
        Язык программирования Python  — это мощный инструмент для создания программ
        самого разнообразного назначения, доступный даже для новичков. С его помощью
        можно решать задачи различных типов.
        </p>
        
        <p>
        Python поддерживает несколько парадигм программирования: структурное,
        объектно‑ориентированное, функциональное, императивное и аспектно‑ориентированное.
        В языке присутствет динамическая типизация, автоматическое управление памятью,
        полная интроспекция, механизм обработки исключений, поддержка многопоточных вычислений
        и удобные высокоуровневые структуры данных. Программный код на Python организовывается
        в функции и классы, которые могут объединяться в модули, а они в свою очередь могут быть
        объединены в пакеты. Python обычно используется как интерпретируемый, но может быть
        скомпилирован в байт‑код Java и в MSIL (в рамках платфоры .NET).
        </p>

        <p>
        По производительности интерпретируемый Python похож на все остальные подобные языки,
        но возможность компиляции в байт‑код позволяет добиться большей производительности.
        </p>

        <img src="''' + url_for('static', filename='pytn.png') + '''">
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''" />

        <footer style="margin-top:20px;">
                &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
        </footer>
      </body>
    </html>
'''

@app.route('/lab1/color')
def colors():
    return '''
<!doctype html>
<html>
    <header>
            НГТУ, ФБ, WEB- программирование, часть 2. 
    </header>
    <body>
        <h1> Воздействие цветов на мозг</h1> <br>
        <p> <b>Черный.</b> Одежда черного цвета стройнит людей, а мозгу помогает принимать более эффективные решения. <br>
            <b>Желтый.</b> Он оказывает самое сильное воздействие на мозг, повышая вашу самооценку и креативность. <br>
            <b>Синий/голубой.</b> Цвет спокойствия, помогает снять стресс и агрессию. В японском городе Нара на одной из опасных улиц города установили синие фонари, после чего количество преступлений снизилось там на 9% <br>
            <b>Зеленый.</b> Снижает усталость, раздражение и физическую боль.Обратите внимание на то, что в больницах часто используют именно голубые и зеленые халаты.<br>
            Покрасьте комнату в <b>фиолетовый</b>  и в ней станет прохладнее. В <b>оранжевый</b> - станет теплее. 
            Эти цвета помогают мозгу сильнее воспринимать температуру.</p> 
        <img src="''' + url_for('static', filename='colors.jpeg') + '''">
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''" />
        <footer>
            &copy; Ткаченко Екатерина, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Ткаченко Екатерина'
    grop_name = 'ФБИ-13'
    lab_numb = '2'
    cour_numb = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price':120},
        {'name': 'апельсины', 'price':80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                           name=name, grop_name=grop_name,
                           lab_numb=lab_numb, cour_numb=cour_numb, fruits=fruits)

@app.route ('/lab2/')
def lab2():
    return render_template('lab2.html')
