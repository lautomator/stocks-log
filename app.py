from flask import Flask
from flask import request
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
import sqlite3
from flask import g

app = Flask(__name__)

# ------------------------------
# Database operations

DATABASE = 'stocks.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# ------------------------------
# Functions

# calculators
# and summary scripts


# ------------------------------
# Views

# main index
@app.route('/')
def index():
    return render_template('index.html')

# record detail
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return render_template('post.html', post_id=post_id)

# calculators
@app.route('/calculators')
def calculators():
    return render_template('calcs.html')

# summary report
@app.route('/report')
def report():
    return render_template('report.html')

# export the log
@app.route('/export')
def export_log():
    return render_template('export.html')
