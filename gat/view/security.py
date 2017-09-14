import random
import string

from flask import Blueprint, render_template, request, redirect, url_for, make_response
from gat.service import security_service
from gat.util import send_email
from gat.dao import dao

security_blueprint = Blueprint('security_blueprint', __name__)


@security_blueprint.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@security_blueprint.route('/login', methods=['POST'])
def login_post():
    if 'email' in request.cookies:
        return render_template('visualizations.html')
    success = security_service.login(request.form.get("email"), request.form.get("password"))
    if success:
        response = make_response(render_template('visualizations.html'))
        response.set_cookie('email', request.form.get("email"), max_age = 1)
        #TODO load user data into visualizations.html
        return response
    return render_template('login.html', error = True)

@security_blueprint.route('/logout')
def logout():
    return redirect(url_for("upload_blueprint.landing_page"))


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
    #TODO verify code from url against database
    code = request.args.get('code', None)
    success = security_service.confirm(code)
    if success:
        return render_template('confirm.html', confirm = True)
    else:
        return render_template('confirm.html', error = True)

@security_blueprint.route('/save')
def save_data():
    case_num = request.args.get('case_num')
    email = request.cookies.get('email')
    if email is not None:
        uidpk = security_service.getData(email)
        security_service.createDirectory(uidpk)
        dao.storeFiles(uidpk, case_num)
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