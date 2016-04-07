from flask import Flask, Blueprint, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, inputs

from app.calculator import FreelanceEntry

from .. models import db

api_mod = Blueprint('api', __name__, url_prefix = '/api')
api = Api(api_mod) # instead of Api(app)

calculation_row = {
	'type' : fields.String,
	'hours' :fields.String,
	'pay'	:fields.String,
	'rate'	:fields.String,
}

calculation_results = {
	'rows' : fields.List(fields.Nested(calculation_row)),
	'total_hours' :  fields.String,
	'total_pay' : fields.String,
}

parser = reqparse.RequestParser()

# HourlyRate
parser.add_argument('hours_worked', type=inputs.regex('^[0-9]+$'))
parser.add_argument('hourly_rate', type=inputs.regex('^[0-9]+$'))

# GuaranteedHours
parser.add_argument('guaranteed_rate', type=inputs.regex('^[0-9]+$'))
parser.add_argument('guaranteed_hours', type=inputs.regex('^[0-9]+$'))
parser.add_argument('actual_hours_worked', type=inputs.regex('^[0-9]+$'))

# for cache = false in ajax get request object (get's around IE's caching)
parser.add_argument('_', type=str)


# Calling parse_args with strict=True ensures that an error is thrown if
# the request includes arguments your parser does not define.
# args = parser.parse_args(strict=True)


class Calculation(Resource):
	@marshal_with(calculation_results)
	def get(self, calculation_type):
		args = parser.parse_args(strict = True)
		if calculation_type == 'hourly_rate':
			entry = FreelanceEntry(
				hourly_rate = args['hours_worked'],
                hours = args['hours_worked'],
                ) 
		elif calculation_type == 'guaranteed_hours':
			entry = FreelanceEntry(
				guaranteed_rate = args['guaranteed_rate'],
                guaranteed_hours = args['guaranteed_hours'],
                hours_worked = args['actual_hours_worked'],
            	)
		calculation = {
			'rows': [],
			'total_hours' : entry.total['hours'],
			'total_pay'   : entry.total['pay'],
			}
		for time_type in ['regular','overtime','doubletime']:
			calculation['rows'].append({
				'type'	: time_type,
				'hours'	: getattr(entry,time_type)['hours'],
				'pay'	: getattr(entry,time_type)['pay'],
				'rate'	: getattr(entry,time_type)['rate'],}
				)
			print(calculation['rows'])
		return calculation, 201

# Setup the API resource routing here
api.add_resource(Calculation, '/calc/<calculation_type>')
