from .. import loader, utils 
from random import choice as какаша


def register(cb):
	cb(PicMod())

class PicMod(loader.Module):
	"""Случайный картинка по аргументам из @pic."""
	strings = {'name': 'Pic'}

	async def piccmd(self, event):
		try:
			args = utils.get_args_raw(event) 
			if not args:
				await event.edit('<b>Нет аргумента после команды.</b>')
				return 
			await event.edit(f'<b>Лови {args}!</b>')
			reslt=await event.client.inline_query('pic',args)
			await reslt[reslt.index(какаша(reslt))].click(event.to_id) 
		except Exception as e:
			await event.edit(str(e)) 
			return 

		


		