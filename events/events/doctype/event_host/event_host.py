# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventHost(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from events.events.doctype.soical_media_link.soical_media_link import SoicalMediaLink
		from frappe.types import DF

		about: DF.TextEditor | None
		address: DF.SmallText | None
		by_line: DF.Data | None
		country: DF.Data | None
		logo: DF.AttachImage | None
		soical_media_links: DF.Table[SoicalMediaLink]
	# end: auto-generated types
	pass
