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
# ref: https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

DATABASE = 'stocks.db'

# ONLY TO BE USED FOR INITIAL OR YEARLY SETUP
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
# ------------------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    # returns a tuple
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(conn, data):
    sql = ''' INSERT INTO stocks_log (
        investment,
        date_entered,
        shares,entry,
        stop,
        target,
        risk_share
        ) VALUES (?, ?, ?, ?, ?, ?, ?); '''

    values = (
       data['investment'],
       data['entry_date'],
       data['shares'],
       data['entry_price'],
       data['stop_price'],
       data['target'],
       data['risk_per_share']
    )

    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


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
    # account value and risk per trade are hard coded for now
    risk_reward = {
        'account_value': 10000,
        'risk_per_trade': .01,
        'risk_per_trade_amt': None,
        'entry': data['entry'],
        'stop': data['stop'],
        'risk_share': data['risk_share'],
        'overall_risk': None,
        'max_shares': None,
        'actual_shares': data['shares'],
        'investment_total': None
    }

    # overall risk = risk per share / entry price
    risk_reward['overall_risk'] = risk_reward['risk_share']\
        / risk_reward['entry']

    # max risk amount per trade (given the account value)
    risk_reward['risk_per_trade_amt'] = risk_reward['account_value']\
        * risk_reward['risk_per_trade']

    return risk_reward

def potential_profits(data):
    pass

def report_summary(data):
    pass

def get_risk_per_share(entry_price, stop_price):
    risk = float(entry_price) - float(stop_price)
    return "{:.2f}".format(risk)



# ------------------------------
# VIEWS

# main page
@app.route('/')
def index():
    sql = 'select * from stocks_log'
    data = query_db(sql)
    return render_template('index.html', data=data)


# record detail
@app.route('/post/<int:post_id>')
def show_post(post_id):
    sql = 'select * from stocks_log where id = ?'
    data = query_db(sql, [post_id], one=True)
    risk_data = risk_reward_calc(data)
    profit_data = {}
    return render_template(
        'post.html',
        post_id=post_id,
        data=data,
        risk_data=risk_data,
        profit_data=profit_data
    )


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
        post_data['risk_per_share'] = get_risk_per_share(
            post_data['entry_price'],
            post_data['stop_price'])

    return render_template(
        'review-add-post.html',
        has_reviewed=has_reviewed,
        post_data=post_data
    )


# CONFIRM a post/record
@app.route('/confirm', methods=['GET', 'POST'])
def confirm_post():
    post_data = {}

    if request.method == 'POST':
        # all of the POST data
        post_data['investment'] = request.form['investment']
        post_data['entry_date'] = request.form['entry_date']
        post_data['shares'] = request.form['shares']
        post_data['entry_price'] = request.form['entry_price']
        post_data['stop_price'] = request.form['stop_price']
        post_data['target'] = request.form['target']
        post_data['risk_per_share'] = request.form['risk_per_share']

        # SQL instertion into DB
        # if response from DB is success, success = True
        # else report any info for debugging
        conn = get_db()
        insert_db(conn, post_data)

    return render_template(
        'confirm-add-post.html',
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





