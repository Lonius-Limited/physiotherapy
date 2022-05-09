# Copyright (c) 2022, Zaha Consulting and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from time import strptime
# import frappe,json
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from datetime import datetime, timedelta

class AppointmentRequest(Document):
	def before_save(self):
		if frappe.get_value("Email Queue",dict(reference_doctype=self.doctype,reference_name=self.name),'name'): return
		self.send_alert()
	def send_alert(self):
		email_args = {
			'recipients': [self.email],
			'sender': "Online Doctors Appointment",
			'subject': "Appointment Request {}".format(self.name or ""),
			'message': self.message,
			'header': [_('Verfication Code'), 'blue'],
			'delayed': False,
			'retry':3
		}

		enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)
		frappe.msgprint(f"{email_args}")
		if frappe.db.get_value('SMS Settings', None, 'sms_gateway_url'):
			send_sms(
					receiver_list=[self.phone],
					msg=self.message
				)

