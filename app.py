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
# DATABASE OPERATIONS

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
# FUNCTIONS

# calculators, summary scripts,
# and app functions

def update_account_details():
    pass

def add_record():
    pass

def edit_record(post_id):
    pass

def delete_record(post_id):
    pass

def risk_reward_calc(data):
    pass

def report_summary(data):
    pass



# ------------------------------
# VIEWS

# main page
@app.route('/')
def index():
    return render_template('index.html')

# account details
@app.route('/account-details', methods=['GET', 'POST'])
def acount_details():
    return render_template('account-details.html')

# record detail
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return render_template('post.html', post_id=post_id)

# summary report
@app.route('/report')
def report():
    return render_template('report.html')

# export the log
@app.route('/export', methods=['GET', 'POST'])
def export_log():
    return render_template('export.html')

# add a post/record
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    return render_template('add-post.html')

# edit a post/record
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    return render_template('edit-post.html', post_id=post_id)

# delete a post/record
@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    return render_template('delete-post.html', post_id=post_id)





