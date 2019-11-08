#!/usr/bin/env python3
from discord.ext import commands

#token here
token = ''

INITIAL_EXTENSIONS = [
        'cogs.log',
        'cogs.bot_help'
        ]

class LogBot(commands.Bot):
    def __init__(self, command_prefix): 
        super().__init__(command_prefix)

        for cog in INITIAL_EXTENSIONS:
            try: 
                self.load_extension(cog)
            except Exception: 
                traceback.print_exc()


    async def on_ready(self): 
        print(self.user.name)


if __name__ == '__main__': 
    bot = LogBot(command_prefix = '!')
    bot.run(token)
