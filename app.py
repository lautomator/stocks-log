from flask import Flask
from flask import request
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template


app = Flask(__name__)

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
