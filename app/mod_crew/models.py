from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from ..models import db
# db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    id              = db.Column(db.Integer, primary_key=True)
    date_create     = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified   = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                            onupdate = db.func.current_timestamp()) 
class Production(Base):
	name = db.Column(db.String(128))
	description = db.Column(db.String(255))
	time_cards = db.relationship('CrewTimeCard', backref="production")

class CrewTimeCard(Base):
	production_id = db.Column(db.Integer, db.ForeignKey('production.id'))
	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref="timecards")

	comments = db.Column(db.String(255))


class CardLine(db.Model):
	id            = db.Column(db.Integer, primary_key=True)
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                            onupdate = db.func.current_timestamp()) 
	cl_date = db.Column(db.Date())

	timestamps = db.relationship('Timestamp', backref="card_line", lazy="dynamic")

	hours = db.relationship('HourCount', backref="card_line", lazy="dynamic")
	
class Timestamp(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	card_line_id = db.Column(db.Integer, db.ForeignKey('card_line.id'))

	type_id = db.Column(db.Integer, db.ForeignKey('timestamp_type.id'))
	type = db.relationship('TimestampType')

	value = db.Column(db.DateTime())

class TimestampType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(25))

class HourCount(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	card_line_id = db.Column(db.Integer, db.ForeignKey('card_line.id'))	
	
	type_id = db.Column(db.Integer, db.ForeignKey('hour_type.id'))
	type = db.relationship('HourType')
	amount = db.Column(db.Float())

class HourType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rate = db.Column(db.Float())
