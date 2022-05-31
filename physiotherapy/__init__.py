
__version__ = '0.0.1'
import frappe
import string
import secrets
def retain_workspace():
	print("Deleting unneccessary workspaces")
	frappe.db.sql("DELETE FROM `tabWorkspace` WHERE module !='Physiotherapy'")
@frappe.whitelist()
def webtoken():
    return frappe.generate_hash()
def randchar():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    return password.lower()
@frappe.whitelist()
def official_email():
    company = default_company()
    default = 'dsmwaura@gmail.com'
    if not company: return default
    return company[0].get("email") or default
@frappe.whitelist()
def official_mobile():
    company = default_company()
    default = '254722810063'
    if not company: return default
    return company[0].get("phone_no") or default
def default_company():
    return frappe.get_all('Company', order_by='creation desc', page_length=1, fields=["*"])
@frappe.whitelist()
def why_us():
    return frappe.get_value('Web Page','why-choose-us','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def proven_evaluation_methods():
    return frappe.get_value('Web Page','proven-evaluation-methods','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def patient_education():
    return frappe.get_value('Web Page','patient-education','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def tailored_treatment_plans():
    return frappe.get_value('Web Page','tailored-treatment-plans','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def about_header():
    return frappe.get_value('Web Page','about-header','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def about_first_paragraph():
    return frappe.get_value('Web Page','about-first-paragraph','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def about_manage_your_pain():
    return frappe.get_value('Web Page','about-manage-your-pain','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def about_improve_your_health():
    return frappe.get_value('Web Page','about-improve-your-health','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def about_move_better_after_surgery():
    return frappe.get_value('Web Page','about-move-better-after-surgery','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def gallery_section():
    return frappe.get_value('Web Page','gallery-section','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def socials_section():
    return frappe.get_value('Web Page','socials-section','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def services_section():
    return frappe.get_value('Web Page','services-section','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def conditions_we_treat():
    return frappe.get_value('Web Page','conditions-we-treat','main_section_html') or '<em>Content Loading</em>'
@frappe.whitelist()
def doctors_list():
    return frappe.get_all("Healthcare Practitioner",filters=dict(status='Active'),fields=["*"], order_by="first_name ASC")
@frappe.whitelist()
def all_services():
    conditions = frappe.get_all('Complaint',filters=dict(is_physiotherapy_condition=1),fields=['name','complaints','web_page','description','webpage_location']) or [dict(complaints='<em>Content Unavailable</em>',description="This means that no data is set up yet", webpage_location="#", data_html='<em>Content Unavailable</em>')]
    if conditions[0].get("complaints") == '<em>Content Loading</em>': return conditions
    for condition in conditions:
        condition['data_html'] = frappe.get_value('Web Page',condition.get("web_page"),'main_section_html')
        condition['service_id'] = randchar()
    return conditions
def append_assessment_form(doc,state):
    # if not doc.get_doc_before_save: return
    name,status,start_date = doc.name, doc.status, doc.start_date
    if name in [x.get('name') for x in frappe.get_all('Patient Assessment Form Treatment Plan', fields=['treatment_plan as name'])]: return
    latest_assessment_form = frappe.get_value("Patient Assessment Form",dict(patient=doc.patient),'name')
    if latest_assessment_form:
        doc = frappe.get_doc('Patient Assessment Form',latest_assessment_form)
        doc.append('treatment_plans_table',dict(treatment_plan=name,start_date=start_date,status=status))
        doc.save(ignore_permissions=True)

