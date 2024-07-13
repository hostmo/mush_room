from mr_config import app
import os
#user
from flask import Flask,request, render_template
#app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
from routes.user import user
app.register_blueprint(user,url_prefix="/user")
app.secret_key = 'doxjjarjeh3die'
from routes.image import image_bp
app.register_blueprint(image_bp, url_prefix="/image")

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/')
def home():
    # 获取闪现消息
    message = request.args.get('message')
    return render_template('login.html', message=message)

if __name__== '__main__':
     app.run(host='0.0.0.0',port=5000,debug=True)

