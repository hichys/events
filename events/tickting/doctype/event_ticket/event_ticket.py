# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		attendee_name: DF.Data | None
		booking: DF.Link | None
		event: DF.Link
		ticket_type: DF.Link
	# end: auto-generated types
	pass
