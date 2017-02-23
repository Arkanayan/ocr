from flask import Flask, request, render_template, flash, redirect, send_file, abort
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg','png','tiff','jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        file_name = "aadhar_file"
        if file_name not in request.files:
            print("no file part")
            return redirect(request.url)
        file = request.files[file_name]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # if is_mp3(file):
            #     file = convert_mp3_to_wav(file)
            # File is accepted
            text = get_text_from_image(filepath)
            return render_template('index.html', text=text)
            
    return render_template('index.html')


def get_text_from_image(path_to_image):
    try:
        from PIL import Image
        import tesserocr
        image = Image.open(path_to_image)
        string = tesserocr.image_to_text(image, lang='eng+hin+kan')
        return string
    except Exception:
        return False