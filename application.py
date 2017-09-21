import matplotlib

matplotlib.use('Agg')

from flask import Flask

from gat.view.gsa import gsa_blueprint
from gat.view.info import info_blueprint
from gat.view.log import log_blueprint
from gat.view.sample import sample_blueprint
from gat.view.sna import sna_blueprint
from gat.view.upload import upload_blueprint
from gat.view.visualize import visualize_blueprint
from gat.view.out import out_blueprint
from gat.view.security import security_blueprint

application = Flask(__name__)
application.register_blueprint(log_blueprint, url_prefix='/log')
application.register_blueprint(info_blueprint)
application.register_blueprint(upload_blueprint)
application.register_blueprint(visualize_blueprint)
application.register_blueprint(sample_blueprint, url_prefix='/sample')
application.register_blueprint(sna_blueprint)
application.register_blueprint(gsa_blueprint)
application.register_blueprint(out_blueprint)
application.register_blueprint(security_blueprint)

#################
#### Running ####
#################

application.secret_key = 'na3928ewafds'

if __name__ == "__main__":
    application.debug = True
    application.run(threaded=True)
