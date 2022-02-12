import csv
import decimal
import requests
import discord
import time
import datetime
from datetime import timedelta
import os
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord_together import DiscordTogether


CountryVirusList = []

x = datetime.datetime.now()
Slash_date = x.strftime("%d"+"/"+"%m"+"/"+"%Y")
time = x.strftime("%I"+":"+"%M"+"%p")
datae = x.strftime("%b"+"%d")
previous_date = datetime.datetime.strptime("01-28-2020", '%m-%d-%Y')
today = datetime.datetime.today()
ndays = (today - previous_date).days

editIDS = [935021235069399100,935021690554032138,935021969651404850,935021985862389820]

yourID = 328696709293015041

def update_csv():
    global my_list, Tconfirmed, Tdeaths
    
    my_list = []
    passed = False
    useDate = today

    Tconfirmed = 0
    Tdeaths = 0
    counter = 0

    while passed == False:
        useDate += timedelta(days=counter)
        CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + datetime.date.strftime(useDate, "%m-%d-%Y") + '.csv'
        
        with requests.Session() as s:
            download = s.get(CSV_URL)

            decoded_content = download.content.decode('utf-8')
            if download.status_code != 404:
                passed = True

            else:
                print('Recieved 404, Retrying...')

        counter-= 1
            
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

def create_dic():
    global Tconfirmed, Tdeaths
    for rangeCount in range(1, len(my_list)):
        CountryCount = []
        CountryCount.append(my_list[rangeCount][3])
        CountryCount.append(my_list[rangeCount][7])
        CountryVirusList.append(CountryCount)

        Tconfirmed = Tconfirmed + int(my_list[rangeCount][7])
        Tdeaths = Tdeaths + int(my_list[rangeCount][8])
        
        if len(CountryVirusList) > 2:
            test1 = CountryVirusList[len(CountryVirusList)-1]
            test2 = CountryVirusList[len(CountryVirusList)-2]
            if test1[0] == test2[0]:
                test2[1] = int(test1[1]) + int(test2[1])
                del CountryVirusList[len(CountryVirusList)- 1]

    for rangeCount in range(0, len(CountryVirusList)):
        CountryVirusList[rangeCount] = Convert(CountryVirusList[rangeCount])
        CountryVirusList[rangeCount]['count'] = int(CountryVirusList[rangeCount]['count'])

def create_message():
    listOfMessages = []
    sortedCountryList = sorted(CountryVirusList, key=lambda d: d['count'], reverse=True)

    listOfMessages.append("**Welcome One and All to the Official Lachclan BioWatch. " + "The Coronavirus BioWatch event is sponsored by Raid Shadow Legends.**\n```yaml\n" + "Coronavirus Stats Updated: " + Slash_date + " " + time + "\n```\n" + "**Confirmed: **" + str(Tconfirmed) + "\n**Deaths: **" + str(Tdeaths) + "\n\n")
    listOfMessages.append("**__Cases:__**\n")
    
    characterCount = 0
    messageCount = 1
    for z in range(0, len(sortedCountryList)):
        thingamabob = ""
        if z == len(sortedCountryList)-5:
            thingamabob = "> **Equestria:** " + str("{:,}".format(sortedCountryList[z]['count'])) + "\n"
            
        thingamabob = thingamabob + "> **" + sortedCountryList[z]['name'] + ":** " + str("{:,}".format(sortedCountryList[z]['count'])) + "\n"
        characterCount+=len(thingamabob)

        if(characterCount > 2000):
            messageCount = messageCount + 1
            listOfMessages.append(thingamabob)
            characterCount=len(thingamabob)

        else:
            listOfMessages[messageCount] += thingamabob

    return listOfMessages
    

def Convert(lst):
    keys = ['name','count']
    res_dct = dict(zip(keys,lst))
    return res_dct

def NewCuntCheck():
    cunts = open("cunts.txt").readlines()
    oldcunts = [r.replace("\n", "") for r in cunts]
    oldcunts.sort()

    newcunts = []
    for rangeCount in range(0, len(CountryVirusList)):
        newcunts.append(CountryVirusList[rangeCount]['name'])
    newcunts.sort()
    list_dif = [i for i in oldcunts + newcunts if i not in oldcunts or i not in newcunts]

    textfile = open("cunts.txt", "w")
    for element in newcunts:
        textfile.write(element + "\n")
    textfile.close()
    
    return list_dif

def updateMessage():

    newcuntslist = NewCuntCheck()
    updateMessage = "**This is Day " + str(ndays+1) + " of our Lachclan Coronavirus BioWatch, " + " as well as more included announcements sponsored by Raid Shadow Legends **"
    updateMessage += "\n```yaml\nAnnouncement: ("+datae+" "+time+")\nOn behalf of the Lachclan BioWatch,"+" we would like to congratulate "
    updateMessage += ', '.join(newcuntslist)
    updateMessage += " on joining the race\n```"

    print(', '.join(newcuntslist) + ' have joined the race, lez gooooooooo')

    return updateMessage
    
class Biowatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.command()
    async def update(self, ctx):
        channel = self.bot.get_channel(537215935199576065)
        if ctx.message.author.id == yourID:
            update_csv()
            create_dic()
            for rangeCount2 in range(0, len(editIDS)):
                message = await channel.fetch_message(editIDS[rangeCount2])
                await message.edit(content=create_message()[rangeCount2])
                
            if NewCuntCheck():
                print("sent update message")
                await channel.send(updateMessage())

            reponse = 'BioWatch Updated :slight_smile:'
            
        else:
           reponse =  'You are not allowed to execute this command :slight_smile:'

        await ctx.send(reponse)
        print('finished updating')

def setup(bot):
    bot.add_cog(Biowatch(bot))
