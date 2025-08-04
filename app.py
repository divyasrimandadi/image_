import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quality = int(request.form.get('quality', 70))
        file = request.files.get('image')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_path = os.path.join(UPLOAD_FOLDER, filename)
            compressed_path = os.path.join(COMPRESSED_FOLDER, filename)

            file.save(original_path)

            # Compress image
            image = Image.open(original_path)
            image.save(compressed_path, optimize=True, quality=quality)

            return render_template(
                'index.html',
                download_url=f'/download/{filename}',
                preview_url=f'/compressed/{filename}',
                filename=filename
            )
        else:
            return render_template('index.html', error='Invalid file format.')

    return render_template('index.html')

@app.route('/compressed/<filename>')
def serve_image(filename):
    return send_from_directory(COMPRESSED_FOLDER, filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(COMPRESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
