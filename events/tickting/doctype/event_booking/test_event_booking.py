# Copyright (c) 2025, awad@hotmail.it and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestEventBooking(FrappeTestCase):
	def test_total_calculation(self):
		TEST_ADDONS_PRICE = 100
		TEST_VIP_TICKET_TYPE_PRICE = 500
		TEST_BOOKING_PRICE = 500
		test_event_category = frappe.get_doc({"doctype": "Event Category", "name": "Test Category"}).insert()
		test_event_venue = frappe.get_doc({"doctype": "Event Venue", "name": "test venu" ,"address": "test Address"}).insert()
		test_event_host = frappe.get_doc({"doctype": "Event Host", "name": "Test Event Host"}).insert()
		test_fe_events = frappe.get_doc(
			{
				"doctype": "FE Events",
				"title": "Test Fe Event",
				"category": test_event_category.name,
				"host": test_event_host.name,
				"venue": test_event_venue.name,
				"start_date": frappe.utils.today(),
			}
		).insert()

		test_ticket_addons = frappe.get_doc(
			{
				"doctype": "Ticket Add-on",
				"title": "T-Shirt",
				"price": TEST_ADDONS_PRICE,
				"event": test_fe_events.name,
			}
		).insert()

		test_ticket_type = frappe.get_doc(
			{
				"doctype": "Event Ticket Type",
				"title": "VIP",
				"event": test_fe_events,
				"currency": "LYD",
				"price": TEST_VIP_TICKET_TYPE_PRICE,
			}
		).insert()
		test_event_booking = frappe.get_doc(
			{
				"doctype": "Event Booking",
				"event": test_fe_events.name,
				"user": "Administrator",
				"attendees": [
					{"ticket_type": test_ticket_type.name, "full_name": "john", "email": "john@jphn.com"},
					{"ticket_type": test_ticket_type.name, "full_name": "jennu", "email": "jennu@jphn.com"},
				],
			}
		).insert()
		#Without Addons
		self.assertEqual(test_event_booking.total_amount ,1000)

		test_attendee_addons = frappe.get_doc({
			"doctype" : "Attendee Ticket Add-ons",
			"add_ons" : [{
				"add_on" : test_ticket_addons.name, "value" : "XL"
			}]
		}).insert()
		test_event_booking.attendees[0].add_ons = test_attendee_addons.name
		test_event_booking.save()

		#TODO enhance values to be dynamic on test changes 
		self.assertEqual(test_event_booking.attendees[0].number_of_add_ons,1)
		self.assertEqual(test_event_booking.attendees[0].add_on_total,TEST_ADDONS_PRICE)
		TEST_NUMBER_OF_ADDONS = 2
		self.assertEqual(test_event_booking.total_amount,TEST_BOOKING_PRICE*TEST_NUMBER_OF_ADDONS+TEST_ADDONS_PRICE)