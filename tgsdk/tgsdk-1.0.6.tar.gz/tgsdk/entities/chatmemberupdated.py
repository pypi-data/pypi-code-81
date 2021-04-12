#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import (
	Optional,
	Dict
)

from tgsdk import TelegramEntity
from tgsdk import (
	User,
	Chat,
	ChatMember,
	ChatInviteLink
)


class ChatMemberUpdated(TelegramEntity):
	"""
	https://core.telegram.org/bots/api#chatmember

	"""

	__slots__ = ("chat", "from_user", "date", "old_chat_member", "new_chat_member", "invite_link")

	def __init__(
		self,
		chat: Chat,
		from_user: User,
		date: int,
		old_chat_member: ChatMember,
		new_chat_member: ChatMember,
		invite_link: ChatInviteLink = None
	):
		self.chat = chat
		self.from_user = from_user
		self.date = date
		self.old_chat_member = old_chat_member
		self.new_chat_member = new_chat_member
		self.invite_link = invite_link

	@classmethod
	def de_json(cls, data: Optional[Dict] = None):
		if not data:
			return None

		data["chat"] = User.de_json(data.get("chat"))
		data["from_user"] = User.de_json(data.get("from"))
		data["old_chat_member"] = User.de_json(data.get("old_chat_member"))
		data["new_chat_member"] = User.de_json(data.get("new_chat_member"))
		data["invite_link"] = User.de_json(data.get("invite_link"))

		return cls(**data)
