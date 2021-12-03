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

def format_currency(amt):
    if amt < 0:
        formatted = "({:,.2f})".format(amt)
    else:
        formatted = "{:,.2f}".format(amt)
    return formatted


def add_record():
    pass


def edit_record(post_id):
    pass


def delete_record(post_id):
    pass


def risk_calc(data):
    # account value and risk per trade are hard coded for now
    risk = {
        'account_value': 9800,
        'risk_per_trade': .02,
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
    risk['overall_risk'] = round(risk['risk_share']\
        / risk['entry'], 2)

    # max risk amount per trade (given the account value)
    risk['risk_per_trade_amt'] = risk['account_value']\
        * risk['risk_per_trade']

    risk['max_shares'] = round(risk['risk_per_trade_amt']\
        / risk['risk_share'])

    risk['investment_total'] = round(risk['entry']\
        * risk['actual_shares'], 2)
    return risk


def profit_calc(data):
    potential_profits = {
        '1r': {},
        '2r': {},
        '3r': {},
        '4r': {},
        '5r': {}
    }
    entry_price = data['entry']
    no_of_shares = data['actual_shares']
    risk_perc = data['overall_risk']
    r = 1
    r_max = 5

    def price(level, entry_price, risk_perc):
        result = round((risk_perc * level + 1) * entry_price, 2)
        return result

    def pnl(price, entry_price, no_of_shares):
        result = (price - entry_price) * no_of_shares
        return round(result, 2)

    # 1R - 5R or rMAX
    while (r <= r_max):
        potential_profits[str(r) + 'r']['price'] = price(r, entry_price, risk_perc)
        potential_profits[str(r) + 'r']['pnl']\
        = pnl(potential_profits[str(r) + 'r']['price'], entry_price, no_of_shares)
        r += 1

    return potential_profits


def report_summary(data):
    pass


def get_risk_per_share(entry_price, stop_price):
    risk = float(entry_price) - float(stop_price)
    return format_currency(risk)



# ------------------------------
# VIEWS

# main page
@app.route('/', methods=['GET', 'POST'])
def index():
    opts_order_by = {
        'Investment': 'investment',
        'Entry Date': 'date_entered',
        'Shares': 'shares',
        'Entry': 'entry',
        'Stop': 'stop',
        'Target': 'target',
        'Risk/Share': 'risk_share',
        'Exit': 'exit',
        'Exit Date': 'sell_date',
        'PnL': 'pnl'
    }

    opts_order = {
        'ASC': 'asc',
        'DESC': 'desc'
    }

    # handle any ordering options
    get_options = {
        'orderby': 'date_entered',
        'order': 'desc'
    }

    if request.method == 'POST':
        get_options['orderby'] = request.form['orderby']
        get_options['order'] = request.form['order']
        sql = 'select * from stocks_log order by ' + get_options['orderby']\
            +' ' + get_options['order']
    else:
        sql = 'select * from stocks_log order by date_entered desc'

    data = query_db(sql)
    return render_template(
        'index.html',
        data=data,
        opts_order_by=opts_order_by,
        opts_order=opts_order,
        get_options=get_options
    )


# record detail
@app.route('/post/<int:post_id>')
def show_post(post_id):
    sql = 'select * from stocks_log where id = ?'
    data = query_db(sql, [post_id], one=True)
    risk_data = risk_calc(data)
    profit_data = profit_calc(risk_data)
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
@app.route('/export')
def export_log():
    sql = 'select * from stocks_log order by investment asc'
    data = query_db(sql)
    return render_template('export.html', data=data)


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





