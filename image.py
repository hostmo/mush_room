from flask import Blueprint,session,request, jsonify, send_from_directory, current_app, render_template
from service.classify import ImageClassifier
from service.classify2 import ImageClassifier2
from werkzeug.utils import secure_filename
import os
from models.user import Record

from flask import session, redirect, url_for
image_bp = Blueprint('image', __name__)

ALLOWED_EXTENSIONS = {'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':

        if 'file' not in request.files:
            return jsonify({'code': -1, 'message': 'No file part', 'data': {}})
        user_id = session['user_id']
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': -1, 'message': 'No selected file', 'data': {}})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Get the selected model from the form
            model_type = request.form.get('model')
            print(f"Selected model type: {model_type}")

            try:
                if model_type == 'alexnet':
                    model_path = "./ai/mushroom_alex_32_0.0001.mod"
                    classifier = ImageClassifier(model_path=model_path)
                    model_used='AlexNet'
                elif model_type == 'vgg':
                    model_path = "./ai/mushroom_vgg_64_0.0001.mod"
                    classifier = ImageClassifier2(model_path=model_path)
                    model_used = 'VGG'
                else:
                    return jsonify({'code': -1, 'message': 'Invalid model type selected', 'data': {}})

                predicted_class, confidence = classifier.classify_image(file_path, user_id)
                return jsonify({
                    'code': 0,
                    'predicted_class': predicted_class,
                    'confidence': confidence,
                    'filename': filename,
                    'model_used': model_used
                })
            except Exception as e:
                return jsonify({'code': -1, 'message': f'Error loading model: {e}', 'data': {}})


@image_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@image_bp.route('/records')
def view_records():
    username = session.get('username')
    if username:
        record_class = globals().get(f'Record_{username}')
        if record_class:
            records = record_class.query.filter_by(user_id=username).all()
            return render_template('test.html', records=records)
    return "No records found."
@image_bp.route('/my_records')
def view_my_records():
    username = session.get('username')
    if username:
        # 假设 Record 已经正确导入
        user_records = Record.query.filter_by(user_id=username).all()
        return render_template('user_records.html', user_records=user_records)
    else:
        return redirect(url_for('user.login'))  # 如果未登录则重定向到登录页面