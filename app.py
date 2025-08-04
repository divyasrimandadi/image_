import os
from flask import Flask, render_template, request, send_file
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quality = int(request.form.get('quality', 80))
        image_file = request.files['image']

        if image_file:
            filename = secure_filename(image_file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            output_path = os.path.join(COMPRESSED_FOLDER, filename)

            image_file.save(input_path)

            image = Image.open(input_path)
            image.save(output_path, quality=quality, optimize=True)

            return render_template('index.html', download_url=f'/download/{filename}')
    return render_template('index.html', download_url=None)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(COMPRESSED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
