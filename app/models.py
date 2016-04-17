from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required



db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    id              = db.Column(db.Integer, primary_key=True)
    date_create     = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified   = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                            onupdate = db.func.current_timestamp()) 

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(Base, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(Base, UserMixin):
     
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    invoices = db.relationship('InvoiceDocument', backref='users ',
                                lazy='dynamic')
   


class InvoiceDocument(Base):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    option_selected = db.Column(db.String(50))
    guranteed_rate  = db.Column(db.String(50))
    guranteed_hours = db.Column(db.String(50))
    actual_hours_worked = db.Column(db.String(50))
    hourly_rate = db.Column(db.String(50))
    hours = db.Column(db.String(50))
    creation_date = db.Column(db.String(50))

   
