import requests
import datetime

URL = 'https://mee6.xyz/api/plugins/levels/leaderboard/388923413839872001'


def userLevel(user):
    data = LeaderboardDict.get(user)
    lvl = data[0]
    xp = data[1]
    LevelXP = 0

    x = datetime.datetime.now()
    time = x.strftime("%x") + " " + x.strftime("%H") + ":" + x.strftime("%M")
    
    for count in range(0, lvl+1):
        LevelXP += 5 * (count ** 2) + (50 * count) + 100

    num = LevelXP-xp
    denom = 5 * (lvl ** 2) + (50 * lvl) + 100
    num = denom - num

    percentage = num / denom


    return output

f = open("mee6LevelData.txt", "w")
for userRank in range (0, len(LeaderboardDict.keys())): 
    f.write(userLevel(getList(LeaderboardDict)[userRank]) + "\n")
    
f.close()





