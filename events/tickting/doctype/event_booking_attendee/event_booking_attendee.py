# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventBookingAttendee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		add_on_total: DF.Currency
		add_ons: DF.Link
		amount: DF.Currency
		currency: DF.Link
		email: DF.Data
		full_name: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		ticket_type: DF.Link
	# end: auto-generated types
	pass

	def get_add_on_total(self):
		"""Calculate the total amount for add-ons."""
		if self.add_ons:
			add_ons_list = frappe.get_cached_doc("Attendee Ticket Add-ons", self.add_ons).add_ons
			return sum(add_on.price for add_on in add_ons_list)
		return 0.0