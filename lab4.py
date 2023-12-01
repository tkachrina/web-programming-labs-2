from flask import Blueprint,render_template, request
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4.html')  


@lab4.route('/lab4/login', methods = ['GET','POST']) 
def login(): 
    error_username = None 
    error_password = None 
     
    if request.method == 'GET':  
        return render_template('login.html') 
 
    username = request.form.get('username') 
    password = request.form.get('password') 
     
    if username == 'alex' and password == '123': 
        return render_template('success1.html', username=username) 
     
    if username == '': 
        error_username = "Не введен логин" 
 
    if password == '': 
        error_password = "Не введен пароль" 
     
    error = 'Неверные логин и/или пароль' 
    return render_template('login.html', error = error, error_username = error_username, 
                            error_password = error_password)

@lab4.route('/lab4/fridge', methods= ['GET','POST'])
def fridge():
    error = ''
    if request.method == 'GET':
        return render_template('fridge.html', error=error)
    
    temperature=request.form.get('temperature')

    if temperature == '':
        error = 'Ошибка:не задана температура'
    else:
        temperature = int(temperature)
        if temperature < -12:
            error = "Не удалось установить температуру - слишком низкое значение"
        elif temperature > -1:
            error = 'Не удалось установить температуру - слишком высокое значение'
        elif (temperature >= -12) and (temperature <= -9):
            error = f'Температура установлена: {temperature}❄️❄️❄️'
        elif (temperature >= -8) and (temperature <= -5):
            error = f'Температура установлена: {temperature}❄️❄️'
        elif (temperature >= -4) and (temperature <= -1):
            error = f'Температура установлена: {temperature}❄️'
    return render_template('fridge.html',temperature=temperature, error=error)  

@lab4.route('/lab4/grain', methods= ['GET','POST'])
def grain():
    if request.method == 'GET':
        return render_template('grain.html')
    price = 0
    error = ''
    error1 = ''
    grain = request.form.get('grain')
    weight = request.form.get('weight')

    if weight=='':
        error = "Нужный вес не задан"
        return render_template('grain.html', error=error)
    weight = int(weight)

    if grain == 'barley':
        price = 12000 * weight
    elif grain == 'oats':
        price = 8500 * weight
    elif grain == 'wheat':
        price = 8700 * weight
    else: 
        grain == 'rye'
        price = 14000 * weight
    if weight <=0:
        error = "Значение неверно"
        return render_template('grain.html',error=error)
    elif weight > 500:
        error = "Нужного объема зерна в наличии нет"
        return render_template('grain.html',error=error)
    elif weight > 50:
        price = price - (price * 10/100)
        error1 = "Скидка 10% за больший объем "
    return render_template('grains.html',error=error, price=price, grain=grain, weight=weight, error1=error1)    

@lab4.route('/lab4/grains', methods= ['GET','POST'])
def grains():
    if request.method == 'GET':
        return render_template('grains.html')
    
@lab4.route('/lab4/cookies', methods = ['GET', 'POST'])
def cookies():
    if request.method == 'GET':
        return render_template('cookies.html')

    color = request.form.get('color_text')
    color_bg = request.form.get('color_bg')
    fontsize = request.form.get('font_size')

    headers = {
        'Set-Cookie': [
            'color=' + color + '; path=/',
            'color_bg=' + color_bg + '; path=/',
            'font_size=' + fontsize + '; path=/',
        ],
        'Location': '/lab4/cookies'
    }

    return '', 303, headers

@lab4.route('/lab4/success1')
def success1():
    return render_template('success1.html')
