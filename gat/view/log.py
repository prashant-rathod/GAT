import subprocess

from flask import Blueprint, render_template

log_blueprint = Blueprint('log_blueprint', __name__)


@log_blueprint.route('/server-error')
def server_error():
    return render_template("log.html", title="Server Error", lines=tail('/var/log/nginx/error.log', 100))


@log_blueprint.route('/server-access')
def server_access():
    return render_template("log.html", title="Server Access", lines=tail('/var/log/nginx/access.log', 100))


@log_blueprint.route('/python-out')
def python_out():
    return render_template("log.html", title="Python Out", lines=tail('nohup.out', 100))


def tail(f, n):
    lines = subprocess.check_output("tail -n " + str(n) + " " + f, shell=True).splitlines()
    return [x.decode("utf-8") for x in lines]
