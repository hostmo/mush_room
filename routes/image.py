from flask import Blueprint, request, jsonify, send_from_directory, current_app, render_template, redirect, url_for
from service.classify import ImageClassifier
from werkzeug.utils import secure_filename
import os

image_bp = Blueprint('image', __name__)

ALLOWED_EXTENSIONS = {'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'code': -1, 'message': 'No file part', 'data': {}})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'code': -1, 'message': 'No selected file', 'data': {}})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        classifier = ImageClassifier(model_path='./ai/mushroom_alex_32_0.0001.mod')
        predicted_class, confidence = classifier.classify_image(file_path)
        return render_template('upload.html', predicted_class=predicted_class, confidence=confidence)

    return render_template('upload.html')

@image_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@image_bp.route('/result')
def result():
    predicted_class = request.args.get('predicted_class')
    confidence = request.args.get('confidence')
    return render_template('result.html', predicted_class=predicted_class, confidence=confidence)
