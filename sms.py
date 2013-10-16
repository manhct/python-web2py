import sys
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import TimeoutException, PinRequiredError, IncorrectPinError

def gmsmodem(port=3,baud=115200,pin=None):
	while port<9:
		try:
			print('Connecting to GSM modem on com %s...'%(port+1))
			modem = GsmModem(port,baud)    
			try:
				print('Checking for pin...')
				modem.connect(pin)
				try:
					print('Checking for network coverage...')
					modem.waitForNetworkCoverage(5)
					return modem
				except Exception, e:
					modem.close()
					print e
			except Exception, e:
				print e
		except Exception, e:
			print e
		port+=1
	return None
	
def sendsms(modem, phone_number, text):
	try:
		sms = modem.sendSms(phone_number, text)
	except TimeoutException:
		print('Failed to send message: the send operation timed out')
		modem.close()
		sys.exit(1)
	else:
		if sms.report:
			print('Message sent{0}'.format(' and delivered OK.' if sms.status == SentSms.DELIVERED else ', but delivery failed.'))
		else:
			print('Message sent.')

from plugin_sms import SMS			
sms = SMS()
			
import time
while True:
	imapdb = DAL("imap://sms:ivinh123@ubnd.hatinh.gov.vn:993", pool_size=1)
	imapdb.define_tables()	
	q = imapdb.INBOX.seen == False
	rows = imapdb(q).select()
	print 'SMS have %s mail'%len(rows)
	modem = gmsmodem() if len(rows)>0 else None
	if modem: 
		for row in rows:
			if row.to:
				emails = sms.get_emails(row.to)
				list_phones = []
				for email in emails:
					msg = 'Ban co thu dien tu gui tu %s den %s vao luc %s.'%(row.sender,email,row.created)
					phones = sms.get_phones([email])
					for phone in phones: 
						sendsms(modem,phone,msg)
						time.sleep(1)
					list_phones+=phones	
				emails = sms.get_emails(row.sender)
				phones = sms.get_phones(emails)
				for phone in phones: 
					msg = 'Tin nhan thong bao da duoc gui den cac so %s.'%(list_phones)
					print msg
					sendsms(modem,phone,msg)
					time.sleep(1)
		print('Modem close...')
		modem.close()
		imapdb(q).update(seen=True)
	time.sleep(30) # check every minute
