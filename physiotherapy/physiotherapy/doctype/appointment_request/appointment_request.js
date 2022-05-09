// Copyright (c) 2022, Zaha Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on('Appointment Request', {
	// refresh: function(frm) {

	// }
	onload_post_render:(frm)=>{
		if(frm.doc.status!="Seen"){
			frm.set_value('status', "Seen")
			refresh_field('status')
			frm.save()
		}
	}
});
