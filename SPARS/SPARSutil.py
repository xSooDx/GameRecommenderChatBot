from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import MySQLdb
import gc

ps = PorterStemmer()
tz = RegexpTokenizer('\w+')

def connectDB():
  conn = MySQLdb.connect(
      host="127.0.0.1",
      user="spars",
      passwd="123456",
      db="spars",
      charset='utf8',
  )
  c = conn.cursor(MySQLdb.cursors.DictCursor)

  return c, conn
  
def closeDB(c, conn):
  c.close()
  conn.close()
  gc.collect()

def splitStem(line):
  return [ ps.stem(x) for x in tz.tokenize(line.lower()) ]
  
  
def matchScore(name, kw):
  nkw = splitStem(name)
  score= 0
  for i in kw:
    if i in nkw: score+=1
  score/=len(nkw)
  return score
  
  
def remStopWords(line):
  return [w for w in line if not w in set(stopwords.words('english'))]
  
