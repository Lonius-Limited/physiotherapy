//frm.set_value('transaction_date', frappe.datetime.add_days(frappe.datetime.get_today(), 7) + " 10:00");
frappe.ui.form.on('Patient', {
    refresh:function(frm){
        console.log("Loaded from JS...")
    },
    age_in_years:function(frm){
        let age = frm.doc.age_in_years
        if(!age){
            age = 0
        }
        age = age*365 //Approximate
        frm.set_value('dob', frappe.datetime.add_days(frappe.datetime.get_today(), parseInt(age*-1)));
        refresh_field("dob")
    }
})
// assets/js/custom_scripts/patient