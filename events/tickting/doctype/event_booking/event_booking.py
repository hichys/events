# Copyright (c) 2025, BWH Studios and contributors
# For license information, please see license.txt
import json

import frappe
from frappe import _
from frappe.model.document import Document


class EventBooking(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from events.tickting.doctype.event_booking_attendee.event_booking_attendee import EventBookingAttendee
		from frappe.types import DF

		amended_from: DF.Link | None
		attendees: DF.Table[EventBookingAttendee]
		currency: DF.Link | None
		event: DF.Link
		total_amount: DF.Currency
		user: DF.Link
	# end: auto-generated types

	def validate(self):
		self.set_total()
		self.set_currency()

	def set_currency(self):
		self.currency = self.attendees[0].currency

	def set_total(self):
		self.total_amount = 0
		for attendee in self.attendees:
			self.total_amount += attendee.amount
			if attendee.add_ons:
				attendee.add_on_total = attendee.get_add_on_total()
				attendee.number_of_add_ons = attendee.get_number_of_addons()
				self.total_amount += attendee.add_on_total

	def on_submit(self):
		self.generate_tickets()

	def generate_tickets(self):
		for attendee in self.attendees:
			ticket = frappe.new_doc("Event Ticket")
			ticket.event = self.event
			ticket.booking = self.name
			ticket.ticket_type = attendee.ticket_type
			ticket.attendee_name = attendee.full_name

			if attendee.add_ons:
				add_ons_list = frappe.get_cached_doc("Attendee Ticket Add-on", attendee.add_ons).add_ons
				ticket.add_ons = add_ons_list
			ticket.insert().submit()

	def on_payment_authorized(self, payment_status: str):
		if payment_status in ("Authorized", "Completed"):
			# payment success, submit the booking
			self.update_payment_record()

	def update_payment_record(self):
		request = frappe.get_all(
			"Integration Request",
			{
				"reference_doctype": "Event Booking",
				"reference_docname": self.name,
				# "owner": frappe.session.user,
			},
			order_by="creation desc",
			limit=1,
		)

		if len(request):
			data = frappe.db.get_value("Integration Request", request[0].name, "data")
			data = frappe._dict(json.loads(data))

			payment_gateway = data.get("payment_gateway")
			if payment_gateway == "Razorpay":
				payment_id = "razorpay_payment_id"
			elif "Stripe" in payment_gateway:
				payment_id = "stripe_token_id"
			else:
				payment_id = "order_id"

			frappe.db.set_value(
				"Event Payment",
				data.payment,
				{
					"payment_received": 1,
					"payment_id": data.get(payment_id),
					"order_id": data.get("order_id"),
				},
			)

			try:
				# submit the booking
				self.submit()
			except Exception:
				frappe.log_error(frappe.get_traceback(), _("Booking Failed"))