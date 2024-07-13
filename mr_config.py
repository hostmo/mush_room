from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1:3306/user'
mr_init=SQLAlchemy(app)
