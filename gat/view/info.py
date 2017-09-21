from flask import Blueprint, render_template, request

info_blueprint = Blueprint('info_blueprint', __name__)


@info_blueprint.route('/help')
def help():
    case_num = request.cookies.get('case_num', None)
    return render_template('help.html', case_num=case_num)


@info_blueprint.route('/contact')
def contact():
    case_num = request.cookies.get('case_num', None)
    return render_template('contact_us.html', case_num=case_num)
