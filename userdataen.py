import os
from .. import loader, utils
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest


def register(cb):
    cb(UserDataMod())

class UserDataMod(loader.Module):
    """This module can change your Telegram profile."""
    strings = {'name': 'UserData'}

    async def namecmd(self, message):
        """For .name command, change your first/second name."""
        args = utils.get_args_raw(message).split('/')
        if len(args) == 0:
            return await message.edit('No any args.')
        if len(args) == 1:
            firstname = args[0]
            lastname = ' '
        elif len(args) == 2:
            firstname = args[0]
            lastname = args[1]
        await message.client(UpdateProfileRequest(first_name=firstname, last_name=lastname))
        await message.edit('Name is changed successfully!')


    async def biocmd(self, message):
        """For .bio command, set a new bio for your profile."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit('No any args.')
        await message.client(UpdateProfileRequest(about=args))
        await message.edit('Successfully edited Bio!')


    async def usernamecmd(self, message):
        """For .username command, set a new username."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit('No any args.')
        try:
            await message.client(UpdateUsernameRequest(args))
            await message.edit('Your username was successfully changed!')
        except UsernameOccupiedError:
            await message.edit('This username is already taken!')