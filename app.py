from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app = Flask (__name__)
app.register_blueprint(lab1)

@lab2.route('/lab2/example')
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
                           name=name, grop_name=grop_name,lab_numb=lab_numb, 
                           cour_numb=cour_numb, fruits=fruits, books=books )

books = [
        {'booktitle': 'Евгений Онегин',  'author' : 'Александр Пушкин', 'genre'  : 'Роман',  'numpages' : '456'},
        {'booktitle' : 'Мастер и Маргарита', 'author' : 'Михаил Булгаков', 'genre' : 'Любовный роман', 'numpages' : 480},
        {'booktitle' : 'Преступление и наказание', 'author' : 'Федор Достоевский', 'genre' : 'Роман', 'numpages' : 608},    
        {'booktitle' : 'Война и мир. Том 4', 'author' : 'Лев Толстой', 'genre' : 'Роман', 'numpages' : 416},   
        {'booktitle' : 'Маленький принц', 'author' : ' Антуан де Сент-Экзюпери', 'genre' : 'Сказка', 'numpages' : 128},   
        {'booktitle' : 'Герой нашего времени', 'author' : 'Михаил Лермонтов', 'genre' : 'Роман', 'numpages' : 288},   
        {'booktitle' : 'Двенадцать стульев', 'author' : 'Илья Ильф, Евгений Петров', 'genre' : 'Роман', 'numpages' : 448},
        {'booktitle' : '1984', 'author' : 'Джордж Оруэлл', 'genre' : 'Научная фантастика', 'numpages' : 320},
        {'booktitle' : 'Сто лет одиночества', 'author' : 'Габриэль Маркес', 'genre' : 'Роман', 'numpages' : 544},
        {'booktitle' : 'Гарри Поттер и Кубок огня', 'author' : 'Джоан Роулинг', 'genre' : 'Фэнтази', 'numpages' : 608},
    ]
@lab2.route ('/lab2/')
def lab2():
    return render_template('lab2.html')

@lab2.route ('/lab2/top5myfood')
def favoritefood():
    return render_template('favoritefood.html')
