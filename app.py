import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename
app = Flask(__name__)
uploaded_imgs = 'uploads'
compressed_imgs = 'compressed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(uploaded_imgs, exist_ok=True)
os.makedirs(compressed_imgs, exist_ok=True)
app.config['UPLOAD_FOLDER'] = uploaded_imgs
app.config['COMPRESSED_FOLDER'] = compressed_imgs
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quality = int(request.form.get('quality', 70))
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_path = os.path.join(uploaded_imgs, filename)
            compressed_path = os.path.join(compressed_imgs, filename)
            file.save(original_path)
            # Compressor image
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
    return send_from_directory(compressed_imgs, filename)
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(compressed_imgs, filename, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
