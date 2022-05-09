from time import strptime
import frappe,json
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from datetime import datetime, timedelta

# @frappe.whitelist()
@frappe.whitelist(allow_guest=1)
def conditions_list_test():
	return frappe.get_all("Complaint", fields=["*"])
@frappe.whitelist(allow_guest=1)
def condition_html(condition=None):
	web_page =   frappe.get_value("Complaint",condition,"web_page")

	if not web_page: return "<em>Condition is not set</em>"

	return frappe.get_value("Web Page", web_page,'main_section_html')
@frappe.whitelist(allow_guest=True)
def post_appointment(payload=None):
	title ="Success. Appointment ID: {}"
	text ="Your request has been received successfully.\nWe have sent a confirmation message to your mobile number {} and email {}"
	icon ="success"

	data = json.loads(payload)
	"""
		payload["fullname"] = $('#name').val() || "Not Provided"
		payload["email"] = $('#email').val() 
		payload["phone"] = $('#phone').val() 
		payload["date"] = $('#datepicker').val() 
		payload["doctor"] = $('#doctor').val() || ""
		payload["message"] = $('#message').val() || ""

	"""
	try:
		# print("")
		rate_limit_time = datetime.now() - timedelta(hours=24)
		args =dict(creation = [">=",rate_limit_time])
		or_args = dict(email = data.get("email"),phone = data.get("phone"))

		if frappe.get_all("Appointment Request", filters=args, or_filters=or_args,fields=["*"]):
			title = "Sorry. We already have your request on file !"
			text = "Operation did not complete because there is a pending request tied to the mobile number or email provided.\n\nIf you think that this is in error, please contact us on our details provided on the website."
			icon = "warning"
			return dict(title=title,text=text,icon=icon,button="OK")
		requested_date = datetime.strptime(data.get("date"),'%m/%d/%Y')
		args = dict(
			doctype="Appointment Request",
			patient_name= data.get("fullname"),
			email = data.get("email"),
			phone = data.get("phone"),
			practitioner_requested = data.get("doctor"),
			appointment_date = requested_date,
			message = data.get("message")
			)
		doc = frappe.get_doc(args)
		doc.flags.ignore_permissions=True
		doc.insert()
		frappe.db.commit()
		return dict(title=title.format(doc.name),text=text.format(data.get("phone"),data.get("email")),icon=icon,button="OK")
	except Exception as e:
		title = "Request Unsuccessfull"
		text = f"Operation did not succeed due to a system error. Please try again soon.\n{e}"
		icon = "error"
		return dict(title=title,text=text,icon=icon,button="OK")


def send_alert(user_email,telephone, message,  request_id=None):
	email_args = {
		'recipients': user_email,
		'sender': "Online Doctors Appointment",
		'subject': "Appointment Request {}".format(request_id or ""),
		'message': message,
		'header': [_('Verfication Code'), 'blue'],
		'delayed': False,
		'retry':3
	}

	enqueue(method=frappe.sendmail, queue='short', timeout=300, event=None,
		is_async=True, job_name=None, now=False, **email_args)
	send_sms(
			receiver_list=[telephone],
			msg=message
		)
