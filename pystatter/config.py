__author__ = 'Liam Jones. http://ljones.id.au. me@ljones.id.au.'


class Config(object):
    DEBUG = False
    TESTING = False
    CSV_DIR = './csv_files/'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
