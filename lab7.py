from flask import Blueprint, render_template, request, abort

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/drink')
def drink():
    return render_template('lab7/drink.html')


@lab7.route('/lab7/api', methods = ['POST'])
def api():
    data = request.json

    if data['method'] == 'get-price':
        return get_price(data['params'])
    if data['method'] == 'pay':
        return pay(data['params'])
    if data['method'] == 'refund':
        return refund(data['params'])
    abort(400)


def get_price(params):
    return {"result": calculate_price(params), "error": None}


def calculate_price(params):
    drink = params['drink']
    milk = params['milk']
    sugar = params['sugar']

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if milk:
        price += 30
    if sugar:
        price += 10
    
    return price


def pay(params):
    card_num = params['card_num']
    cvv = params['cvv']
    if len(card_num) != 16 or not card_num.isdigit():
        return {"result": '', "error": "Неверный номер карты"}

    if len(cvv) != 3 or not cvv.isdigit():
        return {"result": '', "error": "Неверный номер CVV/CVC"}

    price = calculate_price(params)
    return {"result": f'С карты {card_num} списано {price} руб', "error": ''}


def refund(params):
    card_num = params['card_num']
    cvv = params['cvv']
    if len(card_num) != 16 or not card_num.isdigit():
        return {"resultt": '', "errorr": "Неверный номер карты"}

    if len(cvv) != 3 or not cvv.isdigit():
        return {"resultt": '', "errorr": "Неверный номер CVV/CVC"}
    price = calculate_price(params)
    return {"resultt": f'Cумма {price} была возвращена на карту {card_num}', "errorr": ''}