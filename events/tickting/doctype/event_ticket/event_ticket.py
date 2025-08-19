# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from events.tickting.doctype.ticket_add_on_value.ticket_add_on_value import TicketAddOnValue
		from frappe.types import DF

		add_ons: DF.Table[TicketAddOnValue]
		amended_from: DF.Link | None
		attendee_name: DF.Data | None
		booking: DF.Link | None
		event: DF.Link
		qr_code: DF.AttachImage | None
		ticket_type: DF.Link
	# end: auto-generated types
	

	def after_insert(self):
		self.generate_qr_code()

	def generate_qr_code(self):
		import io

		import qrcode
		event_title = frappe.db.get_value("FE Events", self.event, "title")
		event_ticket_type = frappe.db.get_value("Event Ticket Type", self.ticket_type, "title")
		# img = qrcode.make(
		# 	f"Event Ticket: {self.name}\n"
		# 	f"Event: {event_title}\n"
		# 	f"Attendee: {self.attendee_name}\n"
		# 	f"Ticket Type: {event_ticket_type}"
		# )
		img = qrcode.make(f'{self.name}')
		qr_code = io.BytesIO()
		img.save(qr_code, format='PNG')
		hex_data =  qr_code.getvalue()
		# attach the QR code image to the document in field qr_code
		qr_code_file =  frappe.get_doc({
			"doctype": "File",
			"content": hex_data,
			"attached_to_doctype": "Event Ticket",
			"attached_to_name": self.name,
			"is_private": 0,
			"attached_to_field": "qr_code",
			"file_name": f"ticket-qr-code-{self.name}.png"
		}).save()

		self.qr_code = qr_code_file.file_url
		self.save()
		frappe.db.commit()


  
  
