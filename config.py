import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# app configurations
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
SECRET_KEY = 'super_secret'
SECURITY_REGISTERABLE  = True


# email configurations
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'testingapphere@gmail.com'
MAIL_PASSWORD = 'thisisatestpassword'
