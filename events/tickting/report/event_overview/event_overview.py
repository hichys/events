# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

import frappe


def execute(filters:dict|None = None):
	columns=  get_colums()
	data = get_data(filters)
	print(data)
	return columns, data

def get_colums() -> list[dict] :
	return [
		{
			"label" : ("event name"),
			"fieldname" : "event",
			"fieldtype" : "Link",
			"options" : "FE Events"
		},
		{
			"label" : ("Number of Tickets Sold"),
			"fieldname" : "num_tickets_sold",
			"fieldtype" : "Int"
		},
		{
			"label" : ("Number of add ons Sold"),
			"fieldname" : "num_of_addons_sold",
			"fieldtype" : "Int"
		},
		{
			"label" : ("Sales"),
			"fieldname" : "sales", 
			"fieldtype" : "Currency"
		}
	]
def get_data(filters : dict ) -> list[dict] :
	event = filters.get("event")

	if event:
		return [event_summery_overview(event)]
	events = frappe.get_all("FE Events",pluck="name")

	data = []
	for event in events:
		summery = event_summery_overview(event)
		summery["event"] = event
		data.append(summery)

	return data

def event_summery_overview(event) -> dict:
	events_tickets = frappe.db.get_all('Event Ticket', filters={"event":event,"docstatus": 1},pluck="name")
	num_tickets_sold = len(events_tickets)

	num_of_addons_sold = frappe.db.get_all("Ticket Add On Value",filters={
		"parenttype" : "Event Ticket",
		"parentfield" : "add_ons",
		"parent" : ["in",events_tickets]
	}, fields=["count(*) as num_of_addons_sold"],pluck="num_of_addons_sold")[0]
	sales = frappe.db.get_all('Event Booking',
						   filters={
							   "docstatus":1 ,
							   "event":event
							   },fields=["sum(total_amount) as sales"],pluck="sales")[0]

	return {"event":event, "num_tickets_sold":num_tickets_sold,"num_of_addons_sold" : num_of_addons_sold, "sales":sales}

