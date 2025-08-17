# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventTicketType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		currency: DF.Link
		event: DF.Link
		name: DF.Int | None
		price: DF.Currency
		title: DF.Data
	# end: auto-generated types
	pass
