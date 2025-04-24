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
@app.route('/<path:subpath>')
@login_required
def index(subpath=''):
    current_path = os.path.join(app.config['UPLOAD_FOLDER'], subpath)
    if not os.path.exists(current_path):
        flash("Directory not found")
        return redirect(url_for('index'))
    
    files = []
    for item in os.listdir(current_path):
        full_path = os.path.join(current_path, item)
        is_dir = os.path.isdir(full_path)
        rel_path = os.path.join(subpath, item) if subpath else item
        files.append({
            'name': item,
            'is_dir': is_dir,
            'path': rel_path
        })

    breadcrumbs = []
    if subpath:
        parts = subpath.split('/')
        current = ''
        for part in parts:
            current = os.path.join(current, part)
            breadcrumbs.append({'name': part, 'path': current})

    return render_template('index.html',
                         files=files,
                         current_path=subpath,
                         breadcrumbs=breadcrumbs)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    current_path = request.form.get('current_path', '')

    if 'file' not in request.files:
        flash("No file part")
        return redirect(url_for('index', subpath=current_path))

    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
        return redirect(url_for('index', subpath=current_path))

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], current_path, file.filename)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    file.save(upload_path)
    flash("File uploaded successfully")
    return redirect(url_for('index', subpath=current_path))

@app.route('/download/<path:filepath>')
@login_required
def download_file(filepath):
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], directory, filename)

    if filename.endswith('.xml.bzip2'):
        try:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
                html_path = temp_html.name

            subprocess.run([
                'oscap', 'xccdf', 'generate', 'report',
                html_path,
                full_path
            ], check=True)

            return_value = send_file(
                html_path,
                as_attachment=True,
                download_name=filename.replace('.xml.bzip2', '.html')
            )

            os.unlink(html_path)
            return return_value

        except subprocess.CalledProcessError as e:
            flash(f"Error converting file: {str(e)}")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Unexpected error: {str(e)}")
            return redirect(url_for('index'))

    return send_from_directory(
        os.path.join(app.config['UPLOAD_FOLDER'], directory),
        filename,
        as_attachment=True
    )
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

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)
