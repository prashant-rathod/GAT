from flask import Blueprint, render_template, request, redirect, url_for
from gat.service import security_service

security_blueprint = Blueprint('security_blueprint', __name__)


@security_blueprint.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@security_blueprint.route('/login', methods=['POST'])
def login_post():
    success = security_service.login(request.form.get("email"), request.form.get("password"))
    if success:
        #TODO load user data into visualizations.html
        return render_template('visualizations.html')
    return render_template('login.html', error = True)

@security_blueprint.route('/logout')
def logout():
    return redirect(url_for("upload_blueprint.landing_page"))


@security_blueprint.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@security_blueprint.route('/register', methods=['POST'])
def register_post():
    success = security_service.register(request.form.get("email"), request.form.get("password"))
    print(success)
    if success:
        #TODO send email
        return render_template('confirm.html', confirm = False)
    return render_template('register.html', error = True)

@security_blueprint.route('/confirm_email')
def confirm_email():
    #TODO verify code from url against database
    pass

@security_blueprint.route('/forgot_password')
def forgot_password():
    pass

'''@security_blueprint.route('/update_preferences', methods = ['POST'])
def update_preferences_post():
    pass

@security_blueprint.route('/update_preferences', methods = ['GET'])
def update_preferences_get():
    pass
'''