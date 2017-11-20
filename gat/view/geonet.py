from flask import Blueprint, render_template, request, jsonify
from gat.service import gsa_service
geonet_blueprint = Blueprint('geonet_blueprint', __name__)


@geonet_blueprint.route('/geonet', methods=['GET', 'POST'])
def get_json():

    case_num = request.args.get('case_num', None)
    gsa_service.geoNetwork(case_num=case_num)

    return render_template('network.html')

