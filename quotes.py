import logging
from .. import loader, utils
import telethon
import requests, io, PIL
from telethon.tl.types import (MessageEntityBold, MessageEntityItalic,
							   MessageEntityMention, MessageEntityTextUrl,
							   MessageEntityCode, MessageEntityMentionName,
							   MessageEntityHashtag, MessageEntityCashtag,
							   MessageEntityBotCommand, MessageEntityUrl,
							   MessageEntityStrike, MessageEntityUnderline,
							   MessageEntityPhone, ChannelParticipantsAdmins,
							   ChannelParticipantCreator, ChannelParticipantAdmin,
							   User, Channel)
							
logger = logging.getLogger(__name__)


def register(cb):
	cb(QuotesMod())


@loader.tds
class QuotesMod(loader.Module):
	"""Quote a message"""
	strings = {"name": "Quotes"}

	async def client_ready(self, client, db):
		self.client = message.client

	@loader.unrestricted
	@loader.ratelimit
	async def quotecmd(self, message):
		args = utils.get_args_raw(message)
		reply = await message.get_reply_message()
		if not reply:
			await utils.answer(message, '<b>Нет реплая</b>')
			return
		await message.edit("<b>Обработка...</b>")
		
			
		if not args or not args.isdigit():
			count = 1
		else:
			count = int(args.strip()) +1
		msgs = []
		cur = reply.id
		cyr = cur + count
		while cur != cyr:
			msg = await message.client.get_messages(message.to_id, ids=cur)
			if msg:
				msgs.append(msg)
			cur += 1
			
		messages = []
		avatars = {}
		for reply in msgs:
			text = reply.raw_text
			entities = parse_entities(reply)
			if reply.fwd_from:
				id = reply.fwd_from.from_id or reply.fwd_from.channel_id
				if not id:
					id = 1234567890
					name = reply.fwd_from.from_name
					pfp = None
				else:
					sender = await message.client.get_entity(id)
					
					name = (sender.first_name + ("" if not sender.last_name else " "+sender.last_name)) if type(sender) == User else sender.title
					pfp = avatars.get(id, None)
					if not pfp:
						pfp = await message.client.download_profile_photo(sender.id, bytes)
						if pfp:
							pfp = 'https://telegra.ph'+requests.post('https://telegra.ph/upload', files={'file': ('file', pfp, None)}).json()[0]['src']
							avatars[id] = pfp
			else:
				id = reply.from_id
				sender = await message.client.get_entity(id)
				name = (sender.first_name + ("" if not sender.last_name else " "+sender.last_name)) if type(sender) == User else sender.title
				pfp = avatars.get(id, None)
				if not pfp:
					pfp = await message.client.download_profile_photo(reply.from_id, bytes)
					if pfp:
						pfp = 'https://telegra.ph'+requests.post('https://telegra.ph/upload', files={'file': ('file', pfp, None)}).json()[0]['src']
						avatars[id] = pfp
			
			image = await check_media(message, reply)
			
			rreply = await reply.get_reply_message()
			if rreply:
				rtext = rreply.raw_text
				rsender = rreply.sender
				rname = (rsender.first_name + ("" if not rsender.last_name else " "+rsender.last_name)) if type(rsender) == User else rsender.title
				rreply = {'author': rname, 'text': rtext}
				
			admintitle = ""
			if message.chat:
				admins = await message.client.get_participants(message.to_id, filter=ChannelParticipantsAdmins)
				if reply.sender in admins:
					admin = admins[admins.index(reply.sender)].participant
					admintitle = admin.rank if admin else ""
					if not admintitle:
						if type(admin) == ChannelParticipantCreator:
							admintitle = "creator" 
						else:
							admintitle = "admin"
			messages.append({
					"text": text,
					"picture": image,
					"reply": rreply,
					"entities": entities,
					"author": {
							"id": id,
							"name": name,
							"adminTitle": admintitle,
							"picture": pfp
								}
							})
					
			
		data = {"messages": messages,
						"maxWidth": 550,
						"scaleFactor": 5,
						"squareAvatar": False,
						"textColor": "white",
						"replyLineColor": "white",
						"adminTitleColor": "#969ba0",
						"messageBorderRadius": 10,
						"pictureBorderRadius": 8,
						"backgroundColor": "#162330"
						}
	
		await message.edit("<b>О б р а б о т к а . . .</b>")
		r = requests.post("https://mishase.me/quote", json=data)
		output = r.content
		out = io.BytesIO()
		out.name = "quote.webp"
		PIL.Image.open(io.BytesIO(output)).save(out, "WEBP")
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()
		
def parse_entities(reply):
	entities = []
	if not reply.entities:
		return []
	for entity in reply.entities:
		entity_type = type(entity)
		start = entity.offset
		end = entity.length
		if entity_type is MessageEntityBold:
			etype = 'bold'
		elif entity_type is MessageEntityItalic:
			etype = 'italic'
		elif entity_type in [MessageEntityUrl, MessageEntityPhone]:
			etype = 'url'
		elif entity_type is MessageEntityCode:
			etype = 'monospace'
		elif entity_type is MessageEntityStrike:
			etype = 'strikethrough'
		elif entity_type is MessageEntityUnderline:
			etype = 'underline'
		elif entity_type in [MessageEntityMention, MessageEntityTextUrl,
							 MessageEntityMentionName, MessageEntityHashtag,
							 MessageEntityCashtag, MessageEntityBotCommand]:
			etype = 'bluetext'
		entities.append({'type': etype, 'offset': start, 'length': end})
	return entities
	

async def check_media(message, reply):
	if reply and reply.media:
		if reply.photo:
			data = reply.photo
		elif reply.document:
			if reply.gif or reply.video or reply.audio or reply.voice:
				return None
			data = reply.media.document
		else:
			return None
	else:
		return None
	if not data or data is None:
		return None
	else:
		data = await message.client.download_file(data, bytes)
		img = io.BytesIO()
		img.name = "img.png"
		try:
			PIL.Image.open(io.BytesIO(data)).save(img, "PNG")
			link = 'https://telegra.ph'+requests.post('https://telegra.ph/upload', files={'file': ('file', img.getvalue(), "image/png")}).json()[0]['src']
			return link
		except:
			return None
		