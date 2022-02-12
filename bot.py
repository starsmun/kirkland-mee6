import discord
import os
from datetime import datetime
from datetime import timedelta
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from discord.utils import get
from discord_together import DiscordTogether


intents = discord.Intents.all()
activity = discord.Streaming(name="All your personal info", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
client = Bot(command_prefix="&", activity=activity, intents=intents)

yourID = 
####################################################################################################################################################################################################################
####################################################################################################################################################################################################################
############################                                                                   #####################################################################################################################                               
############################     ██╗   ██╗███████╗███████╗██╗     ███████╗███████╗███████╗     #####################################################################################################################
############################     ██║   ██║██╔════╝██╔════╝██║     ██╔════╝██╔════╝██╔════╝     #####################################################################################################################
############################     ██║   ██║███████╗█████╗  ██║     █████╗  ███████╗███████╗     #####################################################################################################################
############################     ██║   ██║╚════██║██╔══╝  ██║     ██╔══╝  ╚════██║╚════██║     #####################################################################################################################
############################     ╚██████╔╝███████║███████╗███████╗███████╗███████║███████║     #####################################################################################################################
############################      ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝     #####################################################################################################################
############################                                                                   #####################################################################################################################
####################################################################################################################################################################################################################
####################################################################################################################################################################################################################



@client.command()
async def say(ctx, *, inputstring):
    if ctx.message.author.id == yourID:
        await ctx.message.delete()
        await ctx.send(inputstring)

@client.event
async def on_member_join(member):
        channel = client.get_channel(805753133653295106)
        await channel.send('<@' + str(member.id) + '> has joined the server')

@client.event
async def on_member_remove(member):
        channel = client.get_channel(805753133653295106)
        await channel.send('<@' + str(member.id) + '> has left the server')

@client.command()
async def start(ctx):
    link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click the blue link!\n{link}")

@client.command()
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    print(member.avatar)

####################################################################################################################################################################################################################
####################################################################################################################################################################################################################
############################                                                                         ###############################################################################################################
############################     ██████╗ ██╗ ██████╗ ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗     ###############################################################################################################
############################     ██╔══██╗██║██╔═══██╗██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║     ###############################################################################################################
############################     ██████╔╝██║██║   ██║██║ █╗ ██║███████║   ██║   ██║     ███████║     ###############################################################################################################
############################     ██╔══██╗██║██║   ██║██║███╗██║██╔══██║   ██║   ██║     ██╔══██║     ###############################################################################################################
############################     ██████╔╝██║╚██████╔╝╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║     ###############################################################################################################
############################     ╚═════╝ ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ###############################################################################################################
############################                                                                         ###############################################################################################################
####################################################################################################################################################################################################################
####################################################################################################################################################################################################################                                                               

   
@client.event
async def on_ready():
    global startTime
    client.togetherControl = await DiscordTogether(BotToken)
    startTime = datetime.now()
    
    print('Bot is ready.')


##################------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##################
##################------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##################
##################------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##################
##################------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##################
##################------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##################
##################------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##################

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{entension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{entension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(BotToken)
    









        





    
    
    


