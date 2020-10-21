from .. import loader
from asyncio import sleep
import random


def register(cb):
	cb(KickRandomMod())

class KickRandomMod(loader.Module):
	"""Кик рандом."""
	strings = {'name': 'KickRandom'}

	async def kickrandcmd(self, event):
		"""Используй .kickrand, чтобы кикнуть случайного пользователя (может кикнуть вас)."""
		if event.chat:
			chat = await event.get_chat()
			admin = chat.admin_rights
			creator = chat.creator
			if not admin and not creator:
				await event.edit('<b>Я здесь не админ.</b>')
				return
			user = random.choice([i for i in await event.client.get_participants(event.to_id)])
			await event.edit('<b>Кому-то сейчас не повезёт...</b>')
			await sleep(3)

			try:
				await event.client.kick_participant(event.chat_id, user.id)
				await sleep(0.5)
			except:
				await event.edit('<b>У меня нет достаточных прав :с</b>')
				return

			await event.edit(f"<b>Рандом выбрал <a href=\"tg://user?id={user.id}\">{user.first_name}</a>, и он кикнут!</b>")
		else:
			await event.edit('<b>Это не чат!</b>')