# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

import frappe
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

	def on_submit(self):
		self.generate_event_tickets()

	def validate(self):
		self.set_total()
		self.set_currency()

	def set_currency(self):
		# Set currency from the first attendee if available for not fetch default currency
		# fetch default currency if no attendees are present
		if not self.attendees:
			self.currency = frappe.get_cached_value("Company", self.company, "default_currency")
		else:
			self.currency = self.attendees[0].currency

	def set_total(self):
		self.total_amount = 0.0
		for attende in self.attendees:
			self.total_amount += attende.amount

	def generate_event_tickets(self):
		for attendee in self.attendees:
			event_ticket = frappe.new_doc("Event Ticket")
			event_ticket.attendee_name = attendee.full_name
			event_ticket.event = self.event
			event_ticket.booking = self.name
			event_ticket.ticket_type = attendee.ticket_type
			event_ticket.insert().submit()

