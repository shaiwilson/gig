import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'not-so-secret')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
    APPLICATION_SID = os.environ['APPLICATION_SID']
    # authy
    AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(DefaultConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'not-so-secret')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
    APPLICATION_SID = os.environ['APPLICATION_SID']
    # authy
    AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY')

    @staticmethod
    def init_app(app):
        pass


class TestConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False


config_env_files = {
    'test': 'gigaware.config.TestConfig',
    'development': 'gigaware.config.DevelopmentConfig',
}
