from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from functools import wraps
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data')
SAVE_PASS = os.getenv('SAVEPASS')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
        return redirect(url_for('index'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash("File uploaded successfully")
    return redirect(url_for('index'))

@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if bcrypt.check_password_hash(bcrypt.generate_password_hash(SAVE_PASS), password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)

