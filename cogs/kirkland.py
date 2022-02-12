import csv
import requests
import discord
import time
import random
from datetime import datetime
from datetime import timedelta
import pandas as pd
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from discord.utils import get
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from io import BytesIO
from numerize import numerize

df = pd.read_csv('mee6data(Formated).csv')
upTime = 0
debugMode = False

 

class kirkland(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saveDataLoop.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        global df
        newUser = True
        personUser = message.author
        cT = datetime.now()
        cT = cT.strftime("%x, %H:%M")

        if personUser.bot == False:
            for index, row in df.iterrows():
                if df.loc[index, 'id'] == personUser.id:
                    newUser = False
                    useIndex = index
                    
            if newUser:
                await message.channel.send('Adding to database')
                xp = random.randint(15, 25)
                df_length = len(df)
                addUser = [df_length+1,1,xp,personUser.id,personUser.name,personUser.discriminator,personUser.avatar,1,xp,100,xp/100,cT]
                df.loc[df_length] = addUser
                
                if debugMode == True: print(df.loc[df_length])
                df.to_csv('mee6data(Formated).csv', encoding='utf-8', index=False)
                df = pd.read_csv('mee6data(Formated).csv')

            else: 
                lT = datetime.strptime(df.loc[useIndex, 'last_message'], '%x, %H:%M').strftime("%x, %H:%M")
               
                if lT != cT: 
                    df.loc[useIndex, 'last_message'] = cT
                    df.loc[useIndex, 'message_count'] += 1
                    addXP = random.randint(15, 25)

                    df.loc[useIndex, 'total_xp'] += addXP
                    df.loc[useIndex, 'XP/LEVEL'] += addXP
                    if debugMode == True: print('added ', addXP, 'XP to ',df.loc[useIndex, 'username'])
                                    
                    if df.loc[useIndex, 'XP/LEVEL'] > df.loc[useIndex, 'level_requirement']:
                        df.loc[useIndex, 'XP/LEVEL'] = df.loc[useIndex, 'XP/LEVEL'] - df.loc[useIndex, 'level_requirement']
                        if debugMode == True: print(df.loc[useIndex, 'username'], ' went up a level, their level xp is now ', df.iloc[useIndex]['XP/LEVEL'])
                        df.loc[useIndex, 'level'] += 1
                        df.loc[useIndex, 'level_requirement'] = LevelXP = 5 * (df.loc[useIndex, 'level'] ** 2) + (50 * df.loc[useIndex, 'level']) + 100

                    df.loc[useIndex, 'percent'] = df.iloc[useIndex]['XP/LEVEL'] / df.iloc[useIndex]['level_requirement']
                    if useIndex != 0:
                        if df.loc[useIndex, 'total_xp'] > df.loc[useIndex-1, 'total_xp']:
                            df.loc[useIndex, 'rank'] -= 1
                            df.loc[useIndex-1, 'rank'] += 1
                            temp = df.loc[useIndex]
                            df.loc[useIndex] = df.loc[useIndex-1]
                            df.loc[useIndex-1] = temp
                            
                            df.to_csv('mee6data(Formated).csv', encoding='utf-8', index=False)
                            df = pd.read_csv('mee6data(Formated).csv')
                            print(df.loc[useIndex-1, 'username'], ' went up a rank, their rank is now ', df.iloc[useIndex-1]['rank'])

                        

        if newUser == False:
            if lT != cT:
                await self.bot.process_commands(message)

    @commands.command()
    @commands.cooldown(1, 10)
    async def rank(self, ctx, *, member: discord.Member = None):
        firstMessage = True
        
        if not member:
            member = ctx.message.author

        for index, row in df.iterrows():
            if df.loc[index, 'id'] == member.id:
                useIndex = index
            
        template = Image.open('levelStuff/BaseTemplate.png')
        iconMask = Image.open('levelStuff/iconMask.png')
        iconMask.convert(mode=0)
        urlAvatar = 'https://cdn.discordapp.com/avatars/' + str(member.id) + '/' + member.avatar + '.png?size=256'
        response = requests.get(urlAvatar)
        icon = Image.open(BytesIO(response.content)).resize((162,162), Image.ANTIALIAS)
        template.paste(icon, (41, 61), iconMask)

        statusIN = str(member.status)
        status = Image.open('levelStuff/' + statusIN + 'card.png')
        statusMask = Image.open('levelStuff/statusMask.png')
        template.paste(status, (160,170), statusMask)

        bar = Image.open('levelStuff/bar.png')
        barfix = Image.new(mode="RGB", size=(637, 40), color = (72, 75, 78))
        barMask = Image.open('levelStuff/barMask.png')

        position1 = int((1 - float(df.loc[useIndex, 'percent'])) * 637) *-1
        
        barfix.paste(bar,(position1,0), barMask)
        template.paste(barfix, (256,182), barMask)

        draw = ImageDraw.Draw(template)
        lnxDir = "/usr/share/fonts/truetype/freefont/"
        font = ImageFont.truetype(lnxDir + "calibri.ttf", 46)
        draw.text((275, 132),df.loc[useIndex, 'username'],(255,255,255),font=font)
        size_width, size_height = draw.textsize(df.loc[useIndex, 'username'], font)
        font = ImageFont.truetype(lnxDir + "calibri.ttf", 27)
        draw.text((295+size_width, 145),'#'+ f"{df.loc[useIndex, 'discriminator']:04d}",(127,131,132),font=font)

        idStuffText = numerize.numerize(float(df.loc[useIndex, 'level_requirement'])) + ' XP'
        size_width, size_height = draw.textsize(idStuffText, font)
        draw.text((882-size_width, 145),idStuffText,(127,131,132),font=font)

        idStuffText = idStuffText
        font = ImageFont.truetype(lnxDir + "arial.ttf", 39)
        size_width = size_width + 18
        draw.text((882-size_width, 135), '/' ,(127,131,132),font=font)

        idStuffText = numerize.numerize(float(df.loc[useIndex, 'XP/LEVEL'])) + idStuffText
        font = ImageFont.truetype(lnxDir + "calibri.ttf", 27)
        size_width, size_height = draw.textsize(idStuffText, font)
        size_width = size_width + 23
        draw.text((882-size_width, 145), numerize.numerize(float(df.loc[useIndex, 'XP/LEVEL'])),(255,255,255),font=font)

        template.save('stupidcard.png')
        await ctx.send(file=discord.File('stupidcard.png'))
            
        
    @tasks.loop(seconds=60)
    async def saveDataLoop(self):
        global df, upTime
        df.to_csv('mee6data(Formated).csv', encoding='utf-8', index=False)
        df = pd.read_csv('mee6data(Formated).csv')
        upTime += 1

    @commands.command()
    @commands.cooldown(1, 60)
    async def uptime(self,ctx):
        global upTime
        await ctx.send(str(timedelta(minutes=upTime)))

    @commands.command()
    async def saveData(self,ctx):
        global df
        df.to_csv('mee6data(Formated).csv', encoding='utf-8', index=False)
        df = pd.read_csv('mee6data(Formated).csv')   



    @commands.command()
    @commands.cooldown(1, 60)
    async def levels(self, ctx):
        await ctx.send("website currently in the works, I'm not gonna bother with copying much of mee6's design since it'll get replaced with our own design soon™")

'''
    @commands.command()
    async def webupdate(self, ctx):
        if ctx.message.author.id == 328696709293015041:
            print('pog')
            upload_file_list = ['mee6data(Formated).csv']
            for upload_file in upload_file_list:
                gfile = drive.CreateFile({'parents': [{'id': '1pzschX3uMbxU0lB5WZ6IlEEeAUE8MZ-t'}]})
                # Read file and set it as the content of this instance.
                gfile.SetContentFile(upload_file)
                gfile.Upload() # Upload the file.
'''

def setup(bot):
    bot.add_cog(kirkland(bot))








	
