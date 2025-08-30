// Copyright (c) 2025, awad@hotmail.it and contributors
// For license information, please see license.txt

frappe.ui.form.on("Event Booking", {
	refresh(frm) {
		frm.set_query("ticket_type", "attendees", (doc, cdt, cdn) => {
			return {
				filters: {
					event: doc.event,
				},
			};
		});
	},
});
