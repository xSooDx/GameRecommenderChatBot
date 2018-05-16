import json
from SPARSutil import *


def getProductFromID(spars_id):
  query = "select * from product where spars_id = {}"
  c, conn = connectDB()
  c.execute(query.format(spars_id))
  res = c.fetchone()
  closeDB(c,conn)
  return res

def getAllProductsFromIDs(spars_ids):
  query = "select * from product where spars_id in ({})"
  c,conn = connectDB()
  c.execute(query.format(",".join([str(x) for x in spars_ids])))
  res = c.fetchall()
  closeDB(c,conn)
  return res
  

def getSimilarIDs(spars_id):
  sim_query = "select similar from similar where spars_id = {}"
  c, conn = connectDB()
  c.execute(sim_query.format(spars_id))
  sim = sorted(json.loads(c.fetchone()['similar']), key=lambda x: x[1],reverse=True )
  closeDB(c,conn)
  return sim

def getTags(spars_id):
  c,conn = connectDB()
  
  c.execute("select genres, tags from product where spars_id = {}".format(spars_id))
  
  res = c.fetchone()
  
  closeDB(c,conn) 
  genres = []
  print(res)
  if res['genres'] == 'none':
    pass
  else:
    genres = json.loads(res['genres'].replace("'",'"'))
  tags = []
  if res['tags'] == 'none': pass
  else:
    tags = json.loads(res['tags'].replace("'",'"'))
  
  res = []
  for i in genres:
    for j in (splitStem(i)):
      res.append(j)
  for i in tags:
    for j in (splitStem(i)):
      res.append(j)
  
  return set(res)
  
  
  
'''
  matches the given name to its closest spar_id in the database
  returns None if no match
'''
def matchName(name):  
  kw = splitStem(name)
  if len(kw) == 0: return None
  c,conn = connectDB()
  query = "SELECT distinct val from name_index where tag = '{}' "
  res = []

  for i in kw:
    d = set()
    c.execute(query.format(i))
    tmp = c.fetchall()
    for i in tmp:
      d.add(i['val'])
    res.append(d)
    
  fin=res[0]
  for i in range(1,len(res)):
    fin=fin.intersection(res[i])

  q2 = "select app_name from product where spars_id={}"
  name_score = 0
  spars_id = None
  name= ""
  for i in fin:
    c.execute(q2.format(i))
    _n = c.fetchone()['app_name']
    score = matchScore(_n,kw)
    if score > name_score:
      name_score = score
      spars_id=i
      name =  _n
  closeDB(c,conn)
  return spars_id, name  


def searchIDsByIndex(tags,index):
  if type(tags) == str: tags = splitStem(tags)
  
  query = "select val from {} where tag = '{}'"
  c,conn = connectDB()
  res = []
  for i in tags:
    c.execute(query.format(index, i))
    tmp = set()
    for i in c.fetchall():
      tmp.add(i['val'])
    res.append(tmp)
  fin = res[0]
  for i in range(1,len(res)):
    tmp = fin.intersection(res[i])
    if len(tmp) != 0:
      fin = tmp
    else:
      if len(fin) < 2:
        fin = fin.union(res[i])
  
  ratings = []
  q = "select rating from product_rating where spars_id = {}"  
  for i in fin:
    c.execute(q.format(i))
    res = c.fetchone()
    if res:
      ratings.append((i,res['rating']))
    else: ratings.append((i,0))
  
    
  closeDB(c,conn)
  return [ x[0] for x in sorted(ratings, key = lambda x: x[1])]
  
def searchProductsByIndex(tags,index):
  
  ids = searchIDsByIndex(tags,index)
  return getAllProductsFromIDs(ids)
  
def searchIDsByTags(tags):  
  if type(tags)==str: tags = remStopWords(splitStem(tags))
  return searchIDsByIndex(tags,'tag_index')
  
  
def searchIDsByNames(tags):
  return searchIDsByIndex(tags,'name_index')
  
  
def searchIDsByDevs(tags):
  return searchIDsByIndex(tags,'dev_index',)
  
  
def searchIDsByPubs(tags):
  return searchIDsByIndex(tags,'pub_index')


def getProductRating(prodID):
  c,conn = connectDB()
  c.execute("Select rating from product_rating where spars_id = {}".format(prodID))
  res = c.fetchone()
  if not res:
    c.execute("select sentiment from product where spars_id={}".format(prodID))
    res = c.fetchone()
    if res['sentiment'] not in ('Very Positive','Overwhelmingly Positive','Positive','Mostly Positive','Negative','Mostly Negative','Very Negative','Overwhelmingly Negative','Mixed'):
      res = {'rating':0}
    else:
      
      if res['sentiment'] in ('Very Positive','Overwhelmingly Positive'): res = {'rating':5}
      elif res['sentiment'] in ('Positive','Mostly Positive'):res = {'rating':4}
      elif res['sentiment'] == 'Mixed': res = {'rating':3}
      elif res['sentiment'] in ('Negative','Mostly Negative'): res = {'rating':2}
      elif res['sentiment'] in ('Very Negative','Overwhelmingly Negative'): res = {'rating':1}
      
  closeDB(c,conn)
  if res:
    return res['rating']
  else:return None
  
