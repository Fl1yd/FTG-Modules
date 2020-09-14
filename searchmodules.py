from .. import loader, utils 


def register(cb):
	cb(SearchMod()) 
	
class SearchMod(loader.Module):
	"""Поиск контента на канале @ftgmodulesbyfl1yd""" 
	strings = {'name': 'SearchModules'} 

	async def searchcmd(self, message):
		"""Используй .search <название>"""
		try:
			title = utils.get_args_raw(message)
			if not title:
				await message.edit("<b>Нет текста после команды.</b>")
			else:
				chat = message.input_chat
				await [i async for i in message.client.iter_messages("ftgmodulesbyfl1yd", search=title)][0].forward_to(chat)
				await message.delete()
		except:
			await message.edit("<b>Не удалось найти контент.</b>")