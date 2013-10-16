###################################################
# This file was developed by ToanLK
# It is released under BSD, MIT and GPL2 licenses
# Version 0.1 Date: 30/08/2013
###################################################
from gluon import current, HTTP
from html import *
from gluon.dal import Field
import re	 
#####################################################################


class SMS:
	def __init__(self,**attr):
		request = current.request
		self.db = attr.get('db',current.globalenv['db'])
		self.auth = attr.get('auth',current.globalenv['auth'])
		self.migrate = attr.get('migrate',False)
		self.define_sms_email()
	
	def define_sms_email(self):	
		if 'sms_email' in self.db.tables: return self.db.sms_email
		return self.db.define_table('sms_email',
			Field('email'),
			Field('phone','string'),
			#Field('credit','integer',default=0),
			migrate=self.migrate)
	
	def get_emails(self,txt):
		return re.findall(r'[\w\.-]+@[\w\.-]+', txt)
	
	def get_phones(self,emails):
		rows = self.db(self.db.sms_email.email.belongs(emails)).select()
		phones = [row.phone for row in rows]
		return phones
