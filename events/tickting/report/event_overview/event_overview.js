// Copyright (c) 2025, awad@hotmail.it and contributors
// For license information, please see license.txt

frappe.query_reports["Event Overview"] = {
    filters: [
        {
            "fieldname": "event",
            "label": __("Event"),
            "fieldtype": "Link",
            "options": "FE Events"
        }
    ]
};
