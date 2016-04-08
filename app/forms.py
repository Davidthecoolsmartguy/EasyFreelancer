from wtforms import SubmitField, TextField
from flask.ext.wtf import Form
from wtforms.validators import required

class HourlyRateForm(Form):
    hours_worked = TextField('Hours Worked', [required()] )
    hourly_rate = TextField('Houly Rate', [required()])
    submit = SubmitField("submit")
    save_invoice = SubmitField("Save Invoice")
class GuaranteedHoursForm(Form):
    guaranteed_rate = TextField('Guranteed Rate', [required()])
    guaranteed_hours = TextField('Guranteed Hours', [required()])
    actual_hours_worked = TextField('Actual Hours Worked', [required()])
    submit = SubmitField("submit")
    save_invoice = SubmitField("Save Invoice")
