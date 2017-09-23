import random
import string

from flask import Blueprint, render_template, request, redirect, url_for, make_response

from gat.service import io_service
from gat.service import security_service
from gat.util import send_email
from gat.dao import dao

security_blueprint = Blueprint('security_blueprint', __name__)


@security_blueprint.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@security_blueprint.route('/login', methods=['POST'])
def login_post():
    if 'session_id' in request.cookies:
        if security_service.getEmail(request.cookies.get('session_id')) is not None:
            return redirect(url_for('visualize_blueprint.visualize'))
    success = security_service.login(request.form.get("email"), request.form.get("password"))
    if success:
        response = make_response(redirect(url_for('visualize_blueprint.visualize')))
        session_id = 100000 + random.randint(0, 100000)
        response.set_cookie('session_id', str(session_id), max_age = 1)
        case_num = request.cookies.get('case_num', None)
        if case_num is None:
            case_num = 100000 + random.randint(0, 100000)
            response.set_cookie('case_num', str(case_num), max_age = 1)
        io_service.loadDict(request.form.get('email'), case_num)

        return response
    return render_template('login.html', error = True)

@security_blueprint.route('/logout')
def logout():
    case_num = request.cookies.get('case_num')
    email = security_service.getEmail(request.cookies.get('session_id'))
    io_service.storeFiles(case_num, email)
    response = make_response(redirect(url_for("upload_blueprint.landing_page")))
    response.set_cookie('session_id', '', expires_days=0)
    return response


@security_blueprint.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@security_blueprint.route('/register', methods=['POST'])
def register_post():
    random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
    success = security_service.register(request.form.get("email"), request.form.get("password"), random_string)
    if success:
        path = '/confirm?code=' + random_string
        send_email.send_confirmation(request.form.get("email"), path)
        data = security_service.getData(request.form.get("email"))
        security_service.createDirectory(data[0])
        return render_template('confirm.html', confirm = False)
    return render_template('register.html', error = True)

@security_blueprint.route('/confirm')
def confirm_email():
    code = request.args.get('code', None)
    success = security_service.confirm(code)
    if success:
        return render_template('confirm.html', confirm = True)
    else:
        return render_template('confirm.html', error = True)

@security_blueprint.route('/save')
def save_data():
    case_num = request.cookies.get('case_num', None)
    email = security_service.getEmail(request.cookies.get('session_id'))
    if email is not None:
        uidpk = security_service.getData(email)
        security_service.createDirectory(uidpk)
        io_service.storeFiles(uidpk, case_num)
    pass

'''@security_blueprint.route('/forgot_password')
def forgot_password():
    pass

@security_blueprint.route('/update_preferences', methods = ['POST'])
def update_preferences_post():
    pass

@security_blueprint.route('/update_preferences', methods = ['GET'])
def update_preferences_get():
    pass
'''