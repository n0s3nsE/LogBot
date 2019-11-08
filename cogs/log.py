from discord.ext import tasks, commands
import base64
import datetime as dt
import discord
import os
import zipfile


#logfile path here
#logfile_path = '/opt/WOWHoneypot/log/access_log'
logfile_path = '/opt/honeypot/log/access_log'


class MainCog(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    #ログ処理
    def logfile_open(self, time, *args):
        temp = []
        dtime = dt.date.today()

        if args:
            if args[0] == 'all':
                time = 'all'
                
            else:
                dtime = str(args[0])

        else:
            if time == '23':
                dtime = dtime + dt.timedelta(days=-1)

            dtime = dtime.strftime('%Y-%m-%d')

        try:
            with open(logfile_path) as f:
                for fs in f:
                    fsp = fs.split()

                    if time == 'all':
                        body = base64.b64decode(fsp[9]).decode()
                        temp.append('```'+ fsp[0] + ' ' + fsp[1] + '\n' + body + '```')

                    elif time != '':
                        if fsp[0][1:] == dtime and fsp[1][0:2] == time:
                            body = base64.b64decode(fsp[9]).decode()
                            temp.append('```' + fsp[0] + ' ' + fsp[1] + '\n' + body + '```')

                    else:
                        if fsp[0][1:] == dtime:
                            body = base64.b64decode(fsp[9]).decode()
                            temp.append('```' + fsp[0] + ' ' + fsp[1] + '\n' + body + '```')
                
                return temp

        except OSError:
            return False

        
    #log出力がループループする
    @tasks.loop(minutes=1)
    async def lplog(self, ctx):
        now = dt.datetime.now()
        b_now = now + dt.timedelta(hours=-1)
        if now.strftime('%M') == '00':
            await ctx.send(b_now.strftime('%H') + '時台のログです\n')
            sdata = self.logfile_open(b_now.strftime('%H'))
            for sd in sdata:
                await ctx.send(sd)


    #定期実行開始
    @commands.command(name='tmstart')
    async def timer_start(self, ctx):
        """毎時丁度にログを出力"""
        await ctx.send('1時間おきにログを吐きます\nタイマーを終了するときは```!tmstop```\n\n\n')
        self.lplog.start(ctx)

    #定期実行終了
    @commands.command(name='tmstop')
    async def timer_stop(self, ctx):
        """ログの定期出力を停止"""
        self.lplog.stop()
        await ctx.send('ログの定期出力を終了しました\n')

    #!log
    @commands.command()
    async def log(self, ctx, *day):
        """ログを出力する"""
        if day:
            if day[0] == 'all':
                sdata = self.logfile_open('', 'all')
            else: 
                sdata = self.logfile_open('', day[0])
             
        else: 
            sdata = self.logfile_open('')


        if sdata:
            for sd in sdata:
                await ctx.send(sd)
        else: 
            await ctx.send('ファイルが存在しないか開けません')


    #!dllog
#    @commands.command()
#    async def dllog(self, ctx, day=dt.date.today().strftime('%Y-%m-%d')):
#        """ログをzip形式で送信"""
#        try:
#            zlname = 'log' + day + '.zip'
#            with zipfile.ZipFile(zlname, 'w', zipfile.ZIP_DEFLATED) as nzip:
#                nzip.write(logfile_path + day, day + '.log')
#            await ctx.send(file=discord.File(zlname))
#
#            os.remove(zlname)
#            print('zipfile deleted')
#        
#        except OSError:
#            os.remove(zlname)
#            await ctx.send('ファイルが存在ないか開けません')


def setup(bot):
    bot.add_cog(MainCog(bot))
