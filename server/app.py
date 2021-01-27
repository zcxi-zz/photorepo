import os
from shutil import rmtree
from flask import Flask, request, current_app, send_from_directory
from flask.helpers import url_for
from flask.json import jsonify
from flask_cors import CORS
from flask_login import current_user
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
import base64

UPLOADS_DIR = os.path.join(os.path.dirname('app.py'), 'uploads')

app = Flask(__name__, static_folder=UPLOADS_DIR)
CORS(app)

try:  # Reset saved files on each start
    rmtree(UPLOADS_DIR, True)
    os.mkdir(UPLOADS_DIR)
    os.mkdir(os.path.join(UPLOADS_DIR, 'public'))
    os.mkdir(os.path.join(UPLOADS_DIR, 'users'))
except OSError:
    raise

with app.app_context():
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['UPLOAD_DIRECTORY'] = UPLOADS_DIR
    app.config['PUBLIC_DIR'] = os.path.join(current_app.config['UPLOAD_DIRECTORY'], 'public')
    app.config['USER_DIR'] = os.path.join(current_app.config['UPLOAD_DIRECTORY'], 'users')


    @app.route("/query", methods=['GET'])
    def query():
        RESULT = [{}, {}]
        return jsonify({
            'status': 'success',
            'courses': RESULT
        })

    @app.route("/catalog", methods=['GET'])
    def get_all_images():

        file_catalog = os.listdir(current_app.config['PUBLIC_DIR'])
        file_urls = []
        for file_name in file_catalog:
            file_name = os.path.join('public/', file_name)
            file_urls.append({'fileurl': url_for('static', filename=file_name, _external=True)})
        return jsonify({
            'status': 'success',
            'files': file_urls,
        })
    @app.route("/catalog", methods=['POST'])
    def get_encoded_images():
        b64_images = []
        
        image_paths = request.form.getlist('image_paths')
        if image_paths:
            for path in image_paths:
                img = path.split('/')
                img = img[-1]
                with open(os.path.join(current_app.config['PUBLIC_DIR'], img), 'rb') as f:
                    b64image = base64.b64encode(f.read())
                    b64_images.append({'image': b64image})        

        return jsonify({
            'status': 'success',
            'images': b64_images,
        })

    @app.route('/uploads/public/<path:path>')
    def send_file(path):
        return send_from_directory(current_app.config['PUBLIC_DIR'], path)

    @app.route("/upload-image", methods=['POST'])
    def upload_image():
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename != '':
                file_ext = os.path.splitext(uploaded_file.filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    raise BadRequest()
                if not request.args.get('isPrivate'):
                    public_directory = current_app.config['PUBLIC_DIR']
                    uploaded_file.save(os.path.join(public_directory, secure_filename(uploaded_file.filename)))
                else:
                    user_directory = current_app.config['USER_DIR']
                    uploaded_file.save(os.path.join(user_directory, current_user.get_id(), secure_filename(uploaded_file.filename)))

        return jsonify({
            'status': 'success'
        })

    @app.route("/remove", methods=['POST'])
    def deleteImages():

        image_paths = request.form.getlist('image_paths')
        if image_paths:
            for path in image_paths:
                img = path.split('/')
                img = img[-1]
                os.remove(os.path.join(current_app.config['PUBLIC_DIR'], img))
        return jsonify({
            'status': 'success',
        })

    @app.errorhandler(413)
    def file_too_large(e):
        return "File is too large", 413
