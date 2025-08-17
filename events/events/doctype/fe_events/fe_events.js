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

frappe.ui.form.on("FE Events", {
    refresh(frm) {
        set_time_zone(frm);
    },
    });
