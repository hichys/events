import frappe
from payments.utils import get_payment_gateway_controller

from events.tickting.doctype.event_booking.event_booking import EventBooking


def get_payment_gateway_for_event(event: str):
	return frappe.get_cached_value("FE Events", event, "payment_gateway")


def get_controller(payment_gateway):
	return get_payment_gateway_controller(payment_gateway)


@frappe.whitelist()
def get_payment_link_for_booking(booking_id: str) -> str:
	booking_doc: EventBooking = frappe.get_cached_doc("Event Booking", booking_id)
	event_title = frappe.get_cached_value("FE Events", booking_doc.event, "title")
	payment_gateway = get_payment_gateway_for_event(booking_doc.event)
	user_full_name = frappe.get_cached_value("User", frappe.session.user, "full_name")

	payment = record_payment(booking_id, booking_doc.total_amount, booking_doc.currency)
	controller = get_controller(payment_gateway)

	# TODO
	redirect_to = "/app"

	payment_details = {
		"amount": booking_doc.total_amount,
		"title": f"Payment for {event_title}",
		"description": f"{user_full_name}'s payment for booking #{booking_id}",
		"reference_doctype": "Event Booking",
		"reference_docname": booking_id,
		"payer_email": frappe.session.user,
		"payer_name": user_full_name,
		"currency": booking_doc.currency,
		"payment_gateway": payment_gateway,
		"redirect_to": redirect_to,
		"payment": payment.name,
	}
	if payment_gateway == "Razorpay":
		order = controller.create_order(**payment_details)
		payment_details.update({"order_id": order.get("id")})

	url = controller.get_payment_url(**payment_details)

	return url


def record_payment(booking_id: str, amount: float, currency: str):
	payment_doc = frappe.new_doc("Event Payment")
	payment_doc.update(
		{
			"user": frappe.session.user,
			"amount": amount,
			"currency": currency,
			"reference_doctype": "Event Booking",
			"reference_docname": booking_id,
		}
	)
	payment_doc.save(ignore_permissions=True)
	return payment_doc


# TODO: use it later!
def save_address(address):
	filters = {"email_id": frappe.session.user}
	exists = frappe.db.exists("Address", filters)
	if exists:
		address_doc = frappe.get_last_doc("Address", filters=filters)
	else:
		address_doc = frappe.new_doc("Address")

	address_doc.update(address)
	address_doc.update(
		{
			"address_title": frappe.db.get_value("User", frappe.session.user, "full_name"),
			"address_type": "Billing",
			"is_primary_address": 1,
			"email_id": frappe.session.user,
		}
	)
	address_doc.save(ignore_permissions=True)
	return address_doc.name