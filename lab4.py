from flask import Blueprint,render_template, request
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4.html')  


@lab4.route('/lab4/login', methods= ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  
    
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'Alex' and password == '123':
        return render_template('success.html',username=username)
    
    error = 'Неверные логин и/или пароль' 
    return render_template ('login.html', error=error, username=username,password=password)

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

