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


# ADD a post/record
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    return render_template('add-post.html')


# REVIEW a post/record
@app.route('/review', methods=['GET', 'POST'])
def review_post():
    has_reviewed = False
    post_data = {}

    if request.method == 'POST':
        # confirm the submission
        has_reviewed = True

        # all of the POST data
        post_data['investment'] = request.form['investment']
        post_data['entry_date'] = request.form['entry_date']
        post_data['shares'] = request.form['shares']
        post_data['entry_price'] = request.form['entry_price']
        post_data['stop_price'] = request.form['stop_price']
        post_data['target'] = request.form['target']

    return render_template(
        'review-add-post.html',
        has_reviewed=has_reviewed,
        post_data=post_data
    )


# CONFIRM a post/record
@app.route('/confirm', methods=['GET', 'POST'])
def confirm_post():
    post_data = {}
    success = False

    if request.method == 'POST':
        # all of the POST data
        post_data['investment'] = request.form['investment']
        post_data['entry_date'] = request.form['entry_date']
        post_data['shares'] = request.form['shares']
        post_data['entry_price'] = request.form['entry_price']
        post_data['stop_price'] = request.form['stop_price']
        post_data['target'] = request.form['target']

        # SQL instertion into DB
        # if response from DB is success, success = True
        # else report any info for debugging

    return render_template(
        'confirm-add-post.html',
        success=success,
        post_data=post_data
    )


# edit a post/record
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    return render_template('edit-post.html', post_id=post_id)


# delete a post/record
@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    return render_template('delete-post.html', post_id=post_id)





