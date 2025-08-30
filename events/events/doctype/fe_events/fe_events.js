// Copyright (c) 2025, awad@hotmail.it and contributors
// For license information, please see license.txt

function set_time_zone(frm) {
	frappe.call("frappe.geo.country_info.get_country_timezone_info").then(({ message }) => {
		// fetch all timezones and set them in the dropdown as autocomplete options
		frm.fields_dict.time_zone.set_data(message.all_timezones);
		// Set the default timezone to the user's current timezone
		frm.set_value("time_zone", Intl.DateTimeFormat().resolvedOptions().timeZone);
	});
}

function publish_button(frm) {
	const publish_label = frm.doc.is_published ? __("Unpublish") : __("Publish");
	frm.add_custom_button(publish_label, () => {
		frappe.confirm(
			"Are you sure to " + publish_label + " this event?",
			() => {
				// YES clicked
				frm.set_value("is_published", !frm.doc.is_published);
				frm.save();
			},
			() => {
				// NO clicked
			}
		);
	});
}

frappe.ui.form.on("FE Events", {
	refresh(frm) {
		frm.set_query("track","schedule", (doc,cdt,cdn) => {
			return {
				filters :{
					event : doc.name
				}
			} 
		})
		
		set_time_zone(frm);
		publish_button(frm);

		//Scan QR Code
		frm.add_custom_button(__("Scan QR Code"), () => {
			frappe.prompt(
				{
					label: "Track",
					fieldname: "track",
					fieldtype: "Link",
					options: "Event Track",
				},
				(values) => {
					const track = values.track;
					new frappe.ui.Scanner({
						dialog: true, // open camera scanner in a dialog
						multiple: false, // stop after scanning one value
						on_scan(data) {
							// console.log(data.decodedText);
							const ticketId = data.decodedText;
							frm.call("check_in", { ticketId, track })
								.then(() => {
									frappe.show_alert({
										message: __("Check-in successful for ticket: {0}", [
											ticketId,
										]),
										indicator: "green",
									});
								})
								.catch(() => {
									frappe.utils.play_sound("error");
									console.error("Error checking in ticket:", error);
									frappe.show_alert({
										message: __("Error checking in ticket: {0}", [
											error.message,
										]),
										indicator: "red",
									});
								});
						},
					});
				}
			);
		});
	},
});

