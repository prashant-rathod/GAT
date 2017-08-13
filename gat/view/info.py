from flask import Blueprint, render_template

info = Blueprint('info', __name__)

@info.route('/help/<int:case_num>')
def help(case_num):
    return render_template('help.html', case_num = case_num)

@info.route('/contact/<int:case_num>')
def contact(case_num):
    return render_template('contact_us.html', case_num = case_num)