def RegularPay(Hours,HourlyRate):
    if Hours <= 8:
        return Hours * HourlyRate
    elif Hours > 8:
        return (HourlyRate * 8)
    else: return 0
def RegularHours(Hours):
    if Hours <= 8:
        return Hours
    elif Hours > 8:
        return abs((Hours-8)-Hours) 
    else: return 0
def OverTimePay(Hours,HourlyRate):
	if Hours > 8 and Hours <= 12:
		return (Hours - 8) * (HourlyRate * 1.5)
	elif Hours > 12:
	    return (4 * HourlyRate) * 1.5
	else: return 0
def OverTimeHours(Hours):
    if Hours > 8 and Hours <= 12:
        return (Hours - 8)
    elif Hours > 12:
        return 4
    else: return 0
def DoubleTimePay(Hours,HourlyRate):
        if Hours > 12:
            return (Hours - 12) * (HourlyRate * 2)
        else: return 0
def DoubleTimeHours(Hours):
        if Hours > 12:
            return (Hours - 12)
        else: return 0

class FreelanceEntry:
	def __init__(self,**kwargs):
		def regular_pay():
		    if self.hours <= 8:
		        return self.hours * self.hourly_rate
		    elif self.hours > 8:
		        return (self.hourly_rate * 8)
		    else: return 0

		def regular_hours():
		    if self.hours <= 8:
		        return self.hours
		    elif self.hours > 8:
		        return abs((self.hours-8)-self.hours) 
		    else: return 0

		def overtime_pay():
			if self.hours > 8 and self.hours <= 12:
				return (self.hours - 8) * (self.hourly_rate * 1.5)
			elif self.hours > 12:
			    return (4 * self.hourly_rate) * 1.5
			else: return 0

		def overtime_hours():
		    if self.hours > 8 and self.hours <= 12:
		        return (self.hours - 8)
		    elif self.hours > 12:
		        return 4
		    else: return 0

		def doubletime_pay():
		        if self.hours > 12:
		            return (self.hours - 12) * (self.hourly_rate * 2)
		        else: return 0

		def doubletime_hours():
		        if self.hours > 12:
		            return (self.hours - 12)
		        else: return 0
		if kwargs.get('guaranteed_rate',None) and kwargs.get('guaranteed_hours',None) and kwargs.get('hours_worked',None):
			gh = int(kwargs['guaranteed_hours'])
			self.hourly_rate = float(kwargs['guaranteed_rate']) / (RegularHours(gh) + (1.5*(OverTimeHours(gh))))
			self.hours = float(kwargs['hours_worked'])
		elif kwargs.get('hourly_rate',None):
			self.hourly_rate = float(kwargs['hourly_rate'])
			self.hours = float(kwargs['hours'])
		else:
			raise ValueError(kwargs)
		self.regular   =   {'hours':'{:,.2f}'.format(regular_hours())   , 'pay':'{:,.2f}'.format(regular_pay()), 	'rate': '{:,.2f}'.format(self.hourly_rate)}
		self.overtime   =  {'hours':'{:,.2f}'.format(overtime_hours())  , 'pay':'{:,.2f}'.format(overtime_pay()), 	'rate': '{:,.2f}'.format(self.hourly_rate * 1.5)}
		self.doubletime =  {'hours':'{:,.2f}'.format(doubletime_hours()), 'pay':'{:,.2f}'.format(doubletime_pay()), 'rate': '{:,.2f}'.format(self.hourly_rate * 2)}
		self.total = {
			'hours': '{:,.2f}'.format(regular_hours() + overtime_hours() + doubletime_hours()),
			'pay': '{:,.2f}'.format(regular_pay() + overtime_pay() + doubletime_pay())
		}