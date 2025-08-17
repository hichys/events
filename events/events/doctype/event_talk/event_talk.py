# Copyright (c) 2025, awad@hotmail.it and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventTalk(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from events.events.doctype.talk_speaker.talk_speaker import TalkSpeaker
		from frappe.types import DF

		speaker: DF.Table[TalkSpeaker]
		title: DF.Data | None
	# end: auto-generated types
	pass
