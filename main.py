import os
from parser import parse_file
from storage import save_file_to_db
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue
        if not allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_id = save_file_to_db(filename, filepath)
        uploaded_files.append({'filename': filename, 'file_id': file_id})

    if not uploaded_files:
        return jsonify({'error': 'No valid files uploaded'}), 400

    return jsonify({'message': 'Files uploaded', 'files': uploaded_files})


@app.route('/parse/<int:file_id>', methods=['GET'])
def parse(file_id):
    result = parse_file(file_id)
    return jsonify({'parsed_data': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


