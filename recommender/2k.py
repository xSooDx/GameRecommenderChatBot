import sys
sys.path.append('../SPARS')
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from functools import reduce
from SPARS import matchName
import SPARSutil as util
import json

file_name = "steam-200k.csv"

users = set()
games = {}
gamesavg = {}
gameids = {}
data = []
ps = PorterStemmer()
tz = RegexpTokenizer('\w+')

print("reading file..")
with open(file_name) as f:
  for i in f:
    p = i.split(',')
    if p[2] =='play':
      userid = int(p[0])
      gamename = p[1].replace('"','')
      hours = float(p[3])
      if gamename not in games:
        games[gamename] = [hours]
      else:games[gamename].append(hours)
      data.append([userid, gamename, hours, 0,None])

print("matching names...")
print(len(games))
for i in games:
  games[i] = reduce(lambda x,y: x+y, games[i])/len(games[i])
  t= matchName(i)
  if not t[0] == None:
    gameids[i] = t[0]
    print(t)
c,conn = util.connectDB()

print("Calculating ratings...")
for i in data:
  tmp = i[2]/games[i[1]]
  if tmp > 1.5:
    i[3] = 5
  elif tmp >1:
    i[3] = 4
  elif tmp >0.6:
    i[3]=3
  elif tmp >0.2:
    i[3] = 2
  else: i[3] = 1
  
  
  if i[1] not in gamesavg:
    gamesavg[i[1]] = [i[3],1]
  else:
    gamesavg[i[1]][0]+=i[3]
    gamesavg[i[1]][1]+=1
  #print(i)
avgs = {}
with open("p1.txt",'w') as fl:
  
  for i in gameids:
    avg = gamesavg[i][0]/gamesavg[i][1]
    avgs[gameids[i]]=avg
    fl.write("{} {}\n".format(gameids[i],avg))
    

for i in avgs:
  c.execute("Insert into product_rating VALUES ({},{})".format(i,avgs[i]))
conn.commit()

print("Done...")

    
