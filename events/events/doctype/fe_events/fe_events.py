# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FEEvents(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from events.events.doctype.schedule_item.schedule_item import ScheduleItem
		from frappe.types import DF

		about: DF.TextEditor | None
		banner_image: DF.AttachImage | None
		category: DF.Link
		end_date: DF.Date | None
		end_time: DF.Time | None
		host: DF.Link
		is_published: DF.Check
		medium: DF.Literal["In Person", "Online", "Hybrid"]
		name: DF.Int | None
		schedule: DF.Table[ScheduleItem]
		short_description: DF.SmallText | None
		start_date: DF.Date | None
		start_time: DF.Time | None
		time_zone: DF.Autocomplete | None
		title: DF.Data
		venue: DF.Link
	# end: auto-generated types

	@frappe.whitelist()
	def check_in(self,ticketId : str,track : str|None = None):
		frappe.get_doc({
			"doctype" : "Event Check In",
			"ticket" : ticketId,
			"track" : track,
		}).insert().submit()

		print("Check-in successful for ticket:", ticketId)


