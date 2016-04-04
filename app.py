from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.mail import Mail
from wtforms import Form, SubmitField, TextField
# Create app
mail = Mail()
app = Flask(__name__)


#database setup
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/test'
#Secuirty
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
#Flask mail setup
mail = Mail(app)
mail.init_app(app)

app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'testingapphere@gmail.com',
    MAIL_PASSWORD = 'thisisatestpassword',
))



SECURITY_REGISTERABLE = True

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# # Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='matt@nobien.net', password='password')
#     db.session.commit()



#wtforms 
class invoice_hourlyrate(Form):
    hours_worked = TextField('Hours Worked')
    hourly_rate = TextField('Houly Rate')
    submit = SubmitField("submit")

class invoice_a(Form):
    guranteed_rate = TextField('Guranteed Rate')
    guranteed_hours = TextField('Guranteed Hours')
    actual_hours_worked = TextField('Actual Hours Worked')
    submit = SubmitField("submit")


# Views
@app.route('/')
@login_required
def index():
    return render_template('pickoption.html')


@app.route('/hourlyrate',methods=['GET','POST'])
@login_required
def hourlyrate():
    form = invoice_hourlyrate()
    return render_template('hourlyrate.html',form = form)



@app.route('/guaranteedhours',methods=['GET','POST'])
@login_required
def guaranteedhours():
    form = invoice_a()
    return render_template('guaranteedhours.html',form = form)
    
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

if __name__ == '__main__':
    app.run()