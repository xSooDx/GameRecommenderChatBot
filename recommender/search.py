import json
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

prod_file = "products_all.jl"
sim_file = "prod_similar.dat"
index_file = "prod_index.dat"

def loadProdData(prod_file, sim_file):
  products = []
  similarity = []

  with open(prod_file) as prod_data,open(sim_file) as sim_data:
    i = 0

    for line in prod_data:
      pd = json.loads(line)
      sd = json.loads(sim_data.readline())
      pd['similar'] = sd
      products.append(pd)
      #similarity.append(sd)
      i+=1
    for j in sim_data:
      raise Exception('line no. missmatch :' + j)
  
  
  tag_index = {}
  name_idnex = {}
  dev_index = {}
  pub_index = {}
  with open(index_file) as f:
    tag_index = json.loads(f.readline())
    name_index = json.loads(f.readline())
    dev_index = json.loads(f.readline())
    pub_index = json.loads(f.readline())
   
  return products, similarity, tag_index, name_index, dev_index, pub_index

def displayMenu():
  print('1)Search Game')
  print('2)Search Tags')
  print('3)Search Devs')
  print('4)Search Pubs')

def searchIndex(products,index,tags):
  res = []
  if tags[0] in index:
    res = index[tags[0]]
    for i in tags[1:]:
      if i in index:
       res = filter(lambda x: x in index[i] ,res)
      else: return []
  
  result = [ products[x] for x in list(res)[:10]]
  return result

def handleChoice(choice):
  pass


def getSimilar(products, item):
  res = []
  for i in sorted(item['similar'],key=lambda e: e[1]):
    res.append(products[i[0]])
  return res
  
def stem(l):
  ps = PorterStemmer()
  tz = RegexpTokenizer('\w+')
  res = [ ps.stem(x) for y in l for x in tz.tokenize(y.lower())]
  return res
  
if __name__=='__main__':
  products, similarity, tag_i,name_i, dev_i, pub_i = loadProdData(prod_file,sim_file)
  for i in searchIndex(products,name_i,stem(["half","life"])):
    print("NAME:",i['app_name'])
    print("Similar:",end=" ")
    for j in getSimilar(products,i):
      print(j['app_name'],end=", ")
    print()


