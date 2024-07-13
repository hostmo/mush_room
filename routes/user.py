from flask import Blueprint,request,flash, redirect, url_for, session, render_template
import json
from service.user import User_operation

user=Blueprint('user',__name__)
@user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        email = data['email']
        gender = data['gender']
        password = data['password']
        confirmpassword = data['confirmpassword']

        if password != confirmpassword:
            message = '确认密码与密码不一致，请重新输入!'
            return redirect(url_for('user.register', message=message))

        u = User_operation()
        result = u.register(username, email, gender, password)

        if result.json['code'] == 0:
            message = result.json['message']
            return redirect(url_for('user.login', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.register', message=message))
    return render_template('register.html')


@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        u = User_operation()
        result = u.login(username, password)
        if result.json['code'] == 0:
            session['username'] = username
            message = result.json['message']
            return redirect(url_for('upload_form', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.login', message=message))
    return render_template('login.html')

