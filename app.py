import os
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from flask.ext.mail import Mail
from forms import GuaranteedHoursForm, HourlyRateForm

BASE_DIR = os.path.abspath(os.path.dirname(__file__))



SECURITY_REGISTERABLE = True
db = SQLAlchemy()


def create_app():
    # Create app
    app = Flask(__name__)
    mail = Mail(app)


    #database setup
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    #Secuirty
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['SECURITY_REGISTERABLE'] = True
    #Flask mail setup
    mail = Mail(app)
    mail.init_app(app)
    from models import Role, User
    db.init_app(app)
    db.app = app
    app.config.update(dict(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'testingapphere@gmail.com',
        MAIL_PASSWORD = 'thisisatestpassword',
    ))
    # Create database connection object


    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # # Create a user to test with
    #@app.before_first_request
    #def create_user():
    #    db.create_all()
    #    user_datastore.create_user(email='matt@nobien.net', password='password')
    #    db.session.commit()





    # Views
    @app.route('/')
    @login_required
    def index():
        return render_template('pickoption.html')


    @app.route('/hourlyrate',methods=['GET','POST'])
    @login_required
    def hourlyrate():
        form = HourlyRateForm(request.form)
        result = ''
        if form.validate_on_submit():
            result = 40
        return render_template('hourlyrate.html',form = form, result=result)



    @app.route('/guaranteedhours',methods=['GET','POST'])
    @login_required
    def guaranteedhours():
        form = GuaranteedHoursForm(request.form)
        result = ''
        if form.validate_on_submit():
            result = 40
        return render_template('guaranteedhours.html',form = form, result=result)
        
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/blog')
    def blog():
        return render_template('blog.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')


    @app.route('/accountsettings')
    @login_required
    def accountsettings():
        return render_template('accountsettings.html')
    return app

if __name__ == '__main__':
    application = create_app()
    application.run()