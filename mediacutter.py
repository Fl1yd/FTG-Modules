import os
from .. import loader, utils


def register(cb):
	cb(MediaCutterMod())
	
class MediaCutterMod(loader.Module):
	"""Обрезать медиа."""
	strings = {'name': 'MediaCutter'}
	
	async def cutcmd(self, event):
		"""Используй .cut <начало(сек):конец(сек)> <реплай на аудио/видео/гиф>."""
		args = utils.get_args_raw(event).split(':')
		reply = await event.get_reply_message()
		if not reply or not reply.media:
			return await event.edit('Нет реплая на медиа.') 
		if reply.media:
			if args:
				if len(args) == 2:
					try:
						await event.edit('Скачиваем...') 
						smth = reply.file.ext
						await event.client.download_media(reply.media, f'uncutted{smth}')
						if not args[0]:
							await event.edit(f'Обрезаем с 0 сек. по {args[1]} сек....')
							os.system(f'ffmpeg -i uncutted{smth} -ss 0 -to {args[1]} -c copy cutted{smth} -y')
						elif not args[1]:
							end = reply.media.document.attributes[0].duration
							await event.edit(f'Обрезаем с {args[0]} сек. по {end} сек....')
							os.system(f'ffmpeg -i uncutted{smth} -ss {args[0]} -to {end} -c copy cutted{smth} -y')
						else:
							await event.edit(f'Обрезаем с {args[0]} сек. по {args[1]} сек....')
							os.system(f'ffmpeg -i uncutted{smth} -ss {args[0]} -to {args[1]} -c copy cutted{smth} -y') 
						await event.edit('Отправляем...') 
						await event.client.send_file(event.to_id, f'cutted{smth}', reply_to=reply.id) 
						os.system('rm -rf uncutted* cutted*') 
						await event.delete()
					except:
						await event.edit('Этот файл не поддерживается.')
						os.system('rm -rf uncutted* cutted*') 
						return 
				else:
					return await event.edit('Неверно указаны аргументы.')
			else:
				return await event.edit('Нет аргументов')