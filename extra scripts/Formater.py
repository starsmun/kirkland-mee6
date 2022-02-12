import csv
import json
import urllib.request
import pandas as pd
import datetime

from urllib.request import Request, urlopen

req = Request('https://mee6.xyz/api/plugins/levels/leaderboard/388923413839872001', headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)

time = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")


data_json = json.loads(response.read())
df = pd.DataFrame.from_dict(data_json['players'])

df[['XP/LEVEL','level_requirement', 'total_xp']] = pd.DataFrame(df.detailed_xp.tolist(), index= df.index)
df.drop('detailed_xp', inplace=True, axis=1)
df.drop('xp', inplace=True, axis=1)
df.drop('guild_id', inplace=True, axis=1)
df.insert(0, 'last_message', time)
df.insert(0, 'percentage',0)

for index, row in df.iterrows():
    percent = int(df.iloc[index]['XP/LEVEL']) / int(df.iloc[index]['level_requirement'])
    df.loc[index, 'percent'] = round(percent,4)

df_new = df.loc[:, ['level', 'total_xp', 'id', 'username', 'discriminator', 'avatar', 'message_count', 'XP/LEVEL', 'level_requirement','percent', 'last_message']]
df_new.to_csv('mee6data(Formated).csv', encoding='utf-8', index=False)






