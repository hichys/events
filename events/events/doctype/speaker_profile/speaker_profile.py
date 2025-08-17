# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SpeakerProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from events.events.doctype.soical_media_link.soical_media_link import SoicalMediaLink
		from frappe.types import DF

		company: DF.Data | None
		designation: DF.Data | None
		display_image: DF.AttachImage | None
		display_name: DF.Data | None
		featured_: DF.Check
		name: DF.Int | None
		soical_media_links: DF.Table[SoicalMediaLink]
		user: DF.Link | None
	# end: auto-generated types
	pass
