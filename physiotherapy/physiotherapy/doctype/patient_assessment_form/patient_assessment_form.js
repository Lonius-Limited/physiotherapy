// Copyright (c) 2022, Zaha Consulting and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient Assessment Form', {
	// frappe.ui.form.on("Server Sheet", "onload", function(frm) {
	onload(frm) {
		if (frm.doc.is_new()) {
			populateAssistiveDevices(frm)
		}

	},
	assistive_devices_necessary(frm){
		frappe.confirm(
			'If you click Yes, your action will clear/reset the Assistive devices table. Continue?',
			function(){
				frm.doc.assistive_devices_table =[]

				frm.refresh_field('assistive_devices_table')

				populateAssistiveDevices(frm)
			},
			function(){
				show_alert('Thanks, please continue!')
			}
			)
	}

	// onload_post_render: function(frm) {
	// 	frm.fields_dict.items.grid.get_field('perceptions_table').get_query =
	// 		function() {
	// 			return {
	// 				filters: {
	// 					"is_group": 0
	// 				}
	// 			}
	// 		}
	// },
	// perceptions_table_add: function(frm){


	// }
});
frappe.ui.form.on('Patient Assessment Form Perception', {
	perceptions_table_add(frm) {
		// your code here
		// frappe.msgprint("Adding data..")
		frm.set_query("perception", "perceptions_table", function () {
			return {
				"filters": {
					"is_group": 0
				}
			};
		});
		//parent_patient_assessment_form_attribute
	}
})

frappe.ui.form.on('Patient Assessment Form Coordination Test', {
	refresh(frm) {
		// your code here
	},
	coordination_tests_table_add(frm) {
		frm.set_query("test_type", "coordination_tests_table", function () {
			return {
				"filters": {
					"parent_patient_assessment_form_attribute": ["IN", ["Non Equilibrium Test", "Equilibrium Test"]]
				}
			};
		});
	}
})
frappe.ui.form.on('Patient Assessment Form Gait Examination Test', {
	refresh(frm) {
		// your code here
	},
	gait_examination_tests_table_add(frm) {
		frm.set_query("test_type", "gait_examination_tests_table", function () {
			return {
				"filters": {
					"parent_patient_assessment_form_attribute": ["IN", ["Gait Examination"]]
				}
			};
		});
	}
})
frappe.ui.form.on('Patient Assessment Form Treatment Plan', {
	refresh(frm) {
		// your code here
	},
	treatment_plans_table_add(frm){
		frm.set_query("treatment_plan", "treatment_plans_table", function () {
			return {
				"filters": {
					"patient": frm.doc.patient
				}
			};
		});

	}
})
function populateAssistiveDevices(frm){
	frappe.call({
		'method': 'frappe.client.get_list',
		'args': {
			'doctype': 'Patient Assessment Form Attribute',
			'columns': ['*'],
			'filters': [['Patient Assessment Form Attribute', 'parent_patient_assessment_form_attribute', 'IN', ["Assistive Devices"]]]
		},
		'callback': function (res) {

			console.log(res, "....")
			// out =[]
			if (res.message) {
				res.message.forEach(itm => {
					let row = frm.add_child('assistive_devices_table', {
						assistive_device: itm.name,
						// qty: 2
					});

					frm.refresh_field('assistive_devices_table')

				})
				// }
			}
			// var template = "<table><tbody>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td>rows[row][col]</td>{% } %}</tr>{% } %}</tbody></table>",
			//    frm.set_df_property('html_fieldname', 'options', frappe.render(template, {rows: res.message});
			//    frm.refresh_field('html_fieldname');
		}
	})
}