from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bhelp')
    async def bhelp(self, ctx):
        """botの詳しいヘルプを表示"""
        await ctx.send('LogViewerBot\n'\
                        'honeypotへのアクセスログを吐くbotです\n\n'\
                        'コマンド一覧```'\
                        '!bhelp : 詳しいヘルプを表示\n'\
                        '!log [Y-m-d | a]: 引数で指定された日付で保存されているログかすべてのログを表示\n'\
                        '            　　　指定しない場合はコマンドを実行した日のログを表示```')
#                        '!dllog [Y-m-d] : 引数で指定した日付で保存されているログをzip形式で送信\n'\
#                        '                 指定しない場合は実行した日付のログを送信```')

def setup(bot):
    bot.add_cog(HelpCog(bot))
