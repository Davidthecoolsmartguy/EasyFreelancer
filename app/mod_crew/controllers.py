from flask import Flask, Blueprint, request


from app.mod_crew.models import db

crew_mod = Blueprint('crew', __name__, url_prefix = '/crew')
#api = Api(api_mod) # instead of Api(app)