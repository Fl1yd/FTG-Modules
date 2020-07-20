from .. import loader
from asyncio import sleep
@loader.tds
class HeartsMod(loader.Module):
	strings = {"name": "Heart's"}
	@loader.owner
	async def lheartscmd(self, message):
		for _ in range(10):
			for lheart in ['❤', '️🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍']:
				await message.edit(lheart)
				await sleep(3)
	
	async def sheartscmd(self, message):
		for _ in range(10):
			for sheart in ['❤', '️🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍']:
				await message.edit(sheart)
				await sleep(0.3)