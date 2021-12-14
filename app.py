from flask import Flask
from flask import request
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
import sqlite3
from flask import g
import swing_stats_mod


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
        shares,
        entry,
        stop,
        target
        ) VALUES (?, ?, ?, ?, ?, ?); '''

    values = (
       data['investment'],
       data['entry_date'],
       data['shares'],
       data['entry_price'],
       data['stop_price'],
       data['target']
    )

    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


def update_db(conn, data):
    sql = ''' UPDATE stocks_log
        SET investment = ?,
            date_entered = ?,
            shares = ?,
            entry = ?,
            stop = ?,
            target = ?,
            exit = ?,
            exit_date = ?,
            notes = ?,
            chart_url = ?
        WHERE id = ?; '''

    values = (
       data['investment'],
       data['entry_date'],
       data['shares'],
       data['entry_price'],
       data['stop_price'],
       data['target'],
       data['exit'],
       data['exit_date'],
       data['notes'],
       data['chart_url'],
       data['post_id']
    )

    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()


def delete_db_record(conn, post_id):
    sql = 'DELETE FROM stocks_log WHERE id=' + str(post_id)
    cur = conn.cursor()
    cur.execute(sql)
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


def risk_calc(data):
    # account value and risk per trade are hard coded for now
    risk = {
        'risk_per_trade_amt': None,
        'entry': data['entry'],
        'stop': data['stop'],
        'risk_share': get_risk_per_share(data['entry'], data['stop']),
        'overall_risk': None,
        'actual_shares': data['shares'],
        'investment_total': None
    }

    # overall risk = risk per share / entry price
    risk['overall_risk'] = round(risk['risk_share'] / risk['entry'], 2)

    risk['investment_total'] = float(abs(round(risk['entry'] * risk['actual_shares'], 2)))
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

    def price_level(level, entry_price, risk_perc):
        result = float(round((risk_perc * level + 1) * entry_price, 2))
        return result

    # to account for a short sell
    if data['actual_shares'] < 0:
        risk_perc = risk_perc - (risk_perc * 2)

    # 1R - 5R or rMAX
    while (r <= r_max):
        potential_profits[str(r) + 'r']['price'] = price_level(r, entry_price, risk_perc)
        potential_profits[str(r) + 'r']['pnl']\
        = get_pnl(potential_profits[str(r) + 'r']['price'], entry_price, no_of_shares)
        r += 1

    return potential_profits


def get_risk_per_share(entry_price, stop_price):
    risk = abs(float(entry_price) - float(stop_price))
    return risk


def get_pnl(exit_price, entry_price, no_of_shares):
    result = float((exit_price - entry_price) * no_of_shares)
    return round(result, 2)


# ------------------------------
# VIEWS

# main page/index of posts
@app.route('/', methods=['GET', 'POST'])
def index():
    opts_order_by = {
        'Investment': 'investment',
        'Entry Date': 'date_entered',
        'Shares': 'shares',
        'Entry': 'entry',
        'Stop': 'stop',
        'Target': 'target',
        'Exit': 'exit',
        'Exit Date': 'exit_date',
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
    sql = 'select * from stocks_log where id=?'
    data = query_db(sql, [post_id], one=True)
    risk_data = risk_calc(data)
    profit_data = profit_calc(risk_data)
    has_chart = False
    pnl = None

    if data['chart_url'] != 'None':
        has_chart = True

    if data['exit'] != 'None':
        pnl = get_pnl(data['exit'], data['entry'], data['shares'])

    return render_template(
        'post.html',
        post_id=post_id,
        data=data,
        risk_data=risk_data,
        profit_data=profit_data,
        pnl=pnl,
        has_chart=has_chart
    )


# ADD a new post/record
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    return render_template('add-post.html')


# REVIEW a new post/record
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


# CONFIRM a new post/record
@app.route('/confirm', methods=['GET', 'POST'])
def confirm_post():
    post_data = {}

    if request.method == 'POST':
        # all of the POST data
        post_data['investment'] = request.form['investment']
        post_data['entry_date'] = request.form['entry_date']
        post_data['shares'] = int(request.form['shares'])
        post_data['entry_price'] = float(request.form['entry_price'])
        post_data['stop_price'] = float(request.form['stop_price'])
        post_data['target'] = float(request.form['target'])

        # SQL instertion into DB
        conn = get_db()
        insert_db(conn, post_data)

    return render_template(
        'confirm-add-post.html',
        post_data=post_data
    )


# edit/update a post/record
@app.route('/edit/<int:post_id>')
def edit_post(post_id):
    sql = 'select * from stocks_log where id=?'
    data = query_db(sql, [post_id], one=True)
    return render_template(
        'edit-post.html',
        post_id=post_id,
        data=data,
    )


# review a post/record update action
@app.route('/review-edit/<int:post_id>', methods=['GET', 'POST'])
def review_update(post_id):
    post_data = {}

    if request.method == 'POST':
        # all of the POST data
        post_data['investment'] = request.form['investment']
        post_data['entry_date'] = request.form['entry_date']
        post_data['shares'] = request.form['shares']
        post_data['entry_price'] = request.form['entry_price']
        post_data['stop_price'] = request.form['stop_price']
        post_data['target'] = request.form['target']
        post_data['exit'] = request.form['exit']
        post_data['exit_date'] = request.form['exit_date']
        post_data['notes'] = request.form['notes']
        post_data['chart_url'] = request.form['chart_url']

    return render_template(
        'review-edit-post.html',
        post_id=post_id,
        post_data=post_data,
    )


# confirm a post/record update action
@app.route('/confirm-edit', methods=['GET', 'POST'])
def confirm_update():
    post_data = {}

    if request.method == 'POST':
        # all of the POST data
        post_data['post_id'] = int(request.form['post_id'])
        post_data['investment'] = request.form['investment']
        post_data['entry_date'] = request.form['entry_date']
        post_data['shares'] = int(request.form['shares'])
        post_data['entry_price'] = float(request.form['entry_price'])
        post_data['stop_price'] = float(request.form['stop_price'])
        post_data['target'] =float(request.form['target'])
        post_data['exit'] = float(request.form['exit'])
        post_data['exit_date'] = request.form['exit_date']
        post_data['notes'] = request.form['notes']
        post_data['chart_url'] = request.form['chart_url']

        # We want to commit a decimal value or None
        if post_data['exit'] =='':
            post_data['exit'] = None

    conn = get_db()
    update_db(conn, post_data)

    return render_template(
        'confirm-edit.html',
        post_data=post_data
    )


# delete a post/record
@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    return render_template('delete-post.html', post_id=post_id)


# CONFIRM deletion
@app.route('/confirm-delete', methods=['GET', 'POST'])
def confirm_delete():
    if request.method == 'POST':
        post_id = request.form['delete_record']
        conn = get_db()
        delete_db_record(conn, post_id)
    return render_template('confirm-delete.html', post_id=post_id)


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

