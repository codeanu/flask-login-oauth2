# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~

    Application Startup config

"""
import os, json, sys
import logging
from gearman import GearmanClient
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import *
from extensions import db, mail

__all__ = ["create_app"]

DEFAULT_APP_NAME = "grexit"


def create_app(config_env=None, app_name=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME


    app = Flask(app_name)

    configure_app(app, config_env)
    configure_logging(app)
    configure_extensions(app)

    app.debug = True

    return app


def configure_app(app, config_env):

    if config_env is not None:
        app.config.from_object('config.' + config_env + 'Config')
    else:
        app.config.from_object('config.DefaultConfig')


def configure_extensions(app):

    mail.init_app(app)
#db.init_app(app)
    #db.app = app #imporant!
    #db = SQLAlchemy(app)
    #oid.init_app(app)
    #cache.init_app(app)
    #configure_i18n(app)
    
class SQLAlchemyHandler(logging.Handler):
    # A very basic logger that just sends a mail
    _app = None

    def __init__(self,app):
        logging.Handler.__init__(self)
        self._app = app

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc(exc)
        logger=record.__dict__['name']
        level=record.__dict__['levelname']
        trace=trace
        msg=record.__dict__['msg']
        to = {'nitesh@grexit.com':'Nitesh Nandy','niraj@grexit.com':'Niraj Ranjan','amitoj@grexit.com':'Amitoj Cheema','anurag@grexit.com' : "Anurag"}
        frm = 'sqlalchemy@grexit.com'
        subject = 'SQL Alchemy Error'
        message = msg + "\n" + str(trace)
        job = dict()
        job['subject'] = subject
        job['bodyText'] = message
        job['bodyHTML'] = message
        job['from'] = frm 
        job['to'] = to
        job['cc'] = dict()
        job['bcc'] = dict()
        json_job=json.dumps(job)
        print "Error found json", json_job
        sys.exit()
        gm_client = GearmanClient(self._app.config['GEARMAN_CRON_HOST'])
        submitted_request = gm_client.submit_job("sendGmailSmtp", json_job,None,None,True,False)
        gm_client.shutdown()

def configure_logging(app):
#if app.debug or app.testing:
#       return

    mail_handler = SQLAlchemyHandler(app)
    mail_handler.setLevel(logging.INFO)
    app.logger.addHandler(mail_handler)

    sqlalchemylogger = logging.getLogger('sqlalchemy.engine')
    sqlalchemylogger.addHandler(mail_handler)
    sqlalchemylogger.setLevel(logging.WARN)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, 
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, 
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)



"""
def configure_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES', 
                                               ['en_gb'])

        return request.accept_languages.best_match(accept_languages)

def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred'))
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("account.login", next=request.path))
"""

