from flask import Blueprint, render_template, request
lab3 = Blueprint ('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    return render_template('lab3.html')

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    errors2 = {}
    age = request.args.get('age')
    if age == '':
        errors2['age'] = 'Заполните поле!'

    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('form1.html', user=user, age=age, sex=sex, errors=errors, errors2=errors2)

@lab3.route('/lab3/order')
def order():
    return render_template('order.html')

@lab3.route('/lab3/pay')
def pay():
    user = request.args.get('user')
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, черный чай - 80 рублей, зеленый - 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавление молока удорожает напиток на 30 рублей, а сахар - на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('pay.html', user=user, price=price)

@lab3.route('/lab3/success')
def success():
    return render_template('success.html')

@lab3.route('/lab3/zd_order')
def zd_order():
    errors = {}
    user = None
    return render_template('zd_order.html', user=user, errors=errors)


@lab3.route('/lab3/zd_pay')
def zd_pay():
    errors = {}

    fio = request.args.get('fio')
    ticketType = request.args.get('ticket-type')
    polkaType = request.args.get('polka')
    withLuggage = request.args.get('with_luggage')
    age = request.args.get('age')
    startPoint = request.args.get('start-point')
    endPoint = request.args.get('end-point')
    date = request.args.get('date')

    user = ZDModel(fio, ticketType, polkaType, withLuggage, age, startPoint, endPoint, date)

    if fio == '':
        errors['fio'] = "Заполните поле!"

    if ticketType is None:
        errors['ticketType'] = "Заполните поле!"

    if polkaType is None:
        errors['polkaType'] = "Заполните поле!"

    if withLuggage is None:
        errors['withLuggage'] = "Заполни поле!"

    if age == '':
        errors['age'] = "Заполни поле!"
    elif int(age) > 120 or int(age) < 1:
        errors['age'] = "Укажи нормальный возраст!"

    if date == '':
        errors['date'] = "Заполни поле!"

    if len(errors) > 0:
        return render_template('zd_order.html', user=user, errors=errors)

    return render_template('zd_success.html', user=user)


@lab3.route('/lab3/zd_success')
def zd_success():
    fio = request.args.get('fio')
    ticketType = request.args.get('ticket-type')
    polkaType = request.args.get('polka')
    withLuggage = request.args.get('with_luggage')
    age = request.args.get('age')
    startPoint = request.args.get('start-point')
    endPoint = request.args.get('end-point')
    date = request.args.get('date')

    user = ZDModel(fio, ticketType, polkaType, withLuggage, age, startPoint, endPoint, date)

    return render_template('zd_success.html', user=user) 

class ZDModel:
    fio = ""
    ticketType = ""
    polkaType = ""
    withLuggage = ""
    age = ""
    startPoint = ""
    endPoint = ""
    date = ""

    def __init__(self, fio, ticketType, polkaType, withLuggage, age, startPoint, endPoint, date):
        self.fio = fio
        self.ticketType = ticketType
        self.polkaType = polkaType
        self.withLuggage = withLuggage
        self.age = age
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.date = date