import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):
    SECRET_KEY = 'secret-key'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TWILIO_ACCOUNT_SID = 'AC8f9b5a52430b59c4275e1a9b8bc7a78a'
    TWILIO_AUTH_TOKEN = 'd78c7e970a38a975aa3e229d5700957c'
    TWILIO_NUMBER = '+12065390536'
    APPLICATION_SID = 'AP73a2377a9d43c2ccb7981ce02513eba3'


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')


class TestConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False


config_env_files = {
    'test': 'gigaware.config.TestConfig',
    'development': 'gigaware.config.DevelopmentConfig',
}
