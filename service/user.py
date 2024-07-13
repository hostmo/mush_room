from models.user import User
from flask import jsonify
from mr_config import mr_init as mr
class User_operation():
    def __init__(self):
        super().__init__()

    def login(self, username, password):
        u = User.query.filter_by(username=username).first()
        if u is None:
            return jsonify({'code': -1, 'message': '用户不存在', 'data':{}})

        u_dict = u.to_dict()
        # print(u_dict)
        if u_dict['password'] != password:
            return jsonify({'code': -2, 'message': '密码错误', 'data': {}})

        return jsonify({'code': 0, 'message': '登录成功', 'data': u_dict})

    def register(self, username, email, gender, password):
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'code': -1, 'message': '用户名已存在！', 'data': {}})
        if existing_email:
            return jsonify({'code': -2, 'message': '邮箱已被注册！', 'data': {}})
        new_user = User(username=username, email=email, gender=gender, password=password)
        mr.session.add(new_user)
        mr.session.commit()
        return jsonify({'code': 0, 'message': '注册成功！', 'data': new_user.to_dict()})

