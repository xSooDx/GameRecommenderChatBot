import MySQLdb
import json
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

sw = "half life"

def connect():
    conn = MySQLdb.connect(
        host="127.0.0.1",
        user="spars",
        passwd="123456",
        db="spars",
        charset='utf8',
    )
    c = conn.cursor(MySQLdb.cursors.DictCursor)

    return c, conn

c,conn = connect()

def getNameScore(name,nm):
  

def searchName(nm):
  if (not type(nm)== list) or len(nm)== 0 : return None
  q = "SELECT distinct val from name_index where tag = '{}' "
  res = []

  for i in nm:
    d = set()
    c.execute(q.format(i))
    tmp = c.fetchall()
    for i in tmp:
      d.add(i['val'])
    res.append(d)
  fin=res[0]
  for i in range(1,len(res)):
    fin=fin.intersection(res[i])
      
  print(fin)
  q2 = "select app_name from product where spars_id={}"
  name_score = 0
  name = ""
  for i in fin:
    c.execute(q2.format(i))
    names.append(c.fetchone()['app-name')
    


    
  

ps = PorterStemmer()
tz = RegexpTokenizer('\w+')
nm = [ ps.stem(x) for x in tz.tokenize("Half life 2".lower())]

searchName(nm)
