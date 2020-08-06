import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    APP_NAME = 'testname for app'

    # >>> import secrets
    # >>> secrets.token_urlsafe()
    SECRET_KEY = 'Iw4nilrNMIYuhsSBQxnxhj0ntOPCjA3Ydmia4li4w4s'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = None
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ADMINS = ['admin@test.de']

    LOG_DIR = 'logs'

    # debug toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_HOSTS = 'http://127.0.0.1:5000'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PANELS = ( 'flask_debugtoolbar.panels.versions.VersionDebugPanel',
                        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
                        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
                        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
                        'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
                        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
                        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
                        'flask_debugtoolbar.panels.logger.LoggingPanel',
                        'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
                        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel'
                      )
    DEBUG_TB_PROFILER_ENABLED = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
