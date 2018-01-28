from flask import Blueprint, send_from_directory

out_blueprint = Blueprint('out_blueprint', __name__)


@out_blueprint.route('/fout/<path:filename>')
def custom_static(filename):
    return send_from_directory("out", filename)
