import os
from flask import Flask, render_template, request,flash,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from flask.ext.mail import Mail
from forms import GuaranteedHoursForm, HourlyRateForm
from calculator import FreelanceEntry
import datetime
timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    # Create app
    app = Flask(__name__)
    mail = Mail(app)
    app.config.from_object('config')
    
    mail = Mail(app)
    mail.init_app(app)

    # db instance is created in models.py (for factory pattern)
    from models import db
    db.init_app(app)


    # Setup Flask-Security
    from models import roles_users, Role, User
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)


    # importmore Moules here
    from models import InvoiceDocument

    # Import modules here
    from app.mod_api.api import api_mod as api_module
    app.register_blueprint(api_module)

    # Views

    # # Create a user to test with
    @app.before_first_request
    def create_user():
      db.create_all()
      user_datastore.create_user(email='matt@nobien.net', password='password')
      user_datastore.create_user(email='test', password='admin')
      db.session.commit()

    @app.route('/')
    @login_required
    def index():
        return render_template('pickoption.html')


    @app.route('/hourly_rate',methods=['GET','POST'])
    @login_required
    def hourly_rate():
        form = HourlyRateForm(request.form)
        entry = None
        if request.method == 'POST':

            if form.validate_on_submit():
                entry = FreelanceEntry(
                hourly_rate = form.hours_worked.data,
                hours = form.hours_worked.data,
                )
                if "submit" in  request.form:
                    flash("button 1 was pressed")
                    return render_template('hourly_rate.html', form=form, entry=entry) 

                if "save_invoice" in request.form:
                    flash("Data Saved ")
                    invoice_saved=InvoiceDocument(option_selected="hourly_rate",hours=form.hours_worked.data,hourly_rate=form.hourly_rate.data,creation_date=timenow)
                    db.session.add(invoice_saved)
                    db.session.commit()
                    return render_template('hourly_rate.html', form=form, entry=entry) 

            else:
                flash("Fill Out both fields")   
                return render_template('hourly_rate.html', form=form, entry=entry) 
    
        elif request.method == 'GET':
            return render_template('hourly_rate.html', form=form, entry=entry)  



    @app.route('/guaranteedhours',methods=['GET','POST'])
    @login_required
    def guaranteed_hours():
        form = GuaranteedHoursForm(request.form)
        entry = None
        if form.validate_on_submit():
            entry = FreelanceEntry(
                guaranteed_rate = form.guaranteed_rate.data,
                guaranteed_hours = form.guaranteed_hours.data,
                hours_worked = form.actual_hours_worked.data,
                )
        return render_template('guaranteedhours.html',form = form, entry=entry)
        
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
