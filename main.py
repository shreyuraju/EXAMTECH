from flask import *
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static'
# ALLOWED_EXTENSIONS = {'pdf','png','jpg', 'jpeg'}
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key' 
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

#index
@app.route('/')
def index():
    # if not os.path.exists(UPLOAD_FOLDER):
    #     os.mkdir(UPLOAD_FOLDER)
    return render_template('index.html')

@app.route('/top')
def top():
    return render_template('top.html')

# @app.route('/left')
# def left():
#     file = os.path(app.config['UPLOAD_FOLDER'])
#     return render_template('left.html', files = file)

@app.route('/left')
def left():
    pdf_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file.endswith('.pdf')]
    return render_template('left.html', pdf_files=pdf_files)

@app.route('/right')
def right():
    return render_template('right.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload/<filename>')
# def upload(filename):
#     return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No File part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No File exist')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
                
            temp_name= "temp"
            type = file.content_type
            type = type[-3:]
            print(type)
            file.filename = temp_name+"."+type
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File Uploaded Successfully')
            return redirect(url_for('top'))
           
        else :
            flash('Connot accept this type of file')
            return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)