import json
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

file_name="products_all.jl"

ps = PorterStemmer()

tz = RegexpTokenizer('\w+')

names = set()
devs = set()
pubs = set()
tags = set()
products = []
num = 0
with open(file_name) as f:
  for line in f:
    jobj = json.loads(line)
    #if num % 100 == 0: print("entry:",num)
    try:
      for g in jobj['genres']:
        for u in tz.tokenize(g.lower()):
          w = ps.stem(u)
          tags.add(w)
    except:
      pass
    try:
      for g in jobj['specs']:
        for u in tz.tokenize(g.lower()):
          w = ps.stem(u)
          tags.add(w)
    except:
      pass
    try:
      for g in jobj['tags']:
        for u in tz.tokenize(g.lower()):
          w = ps.stem(u)
          tags.add(w)
    except:
      pass
    try:
      for u in tz.tokenize(jobj['developer'].lower()):
        w = ps.stem(u)
        devs.add(w)
    except:
      pass
    try:
      for u in tz.tokenize(jobj['publisher'].lower()):
        w = ps.stem(u)
        pubs.add(w)
    except:
      pass
    try:
      for u in tz.tokenize(jobj['app_name'].lower()):
        w = ps.stem(u)
        names.add(w)
    except:
      pass
      
    products.append(jobj)
    num+=1
    #if num == 100: break
    
print(tags)
print(names)
print(devs)
print(pubs)

'''
for key in tag_index:
  tag_index[key] = sorted(list(set(tag_index[key])))
  
for key in dev_index:
  dev_index[key] = sorted(list(set(dev_index[key])))

for key in name_index:
  name_index[key] = sorted(list(set(name_index[key])))
  
for key in pub_index:
  pub_index[key] = sorted(list(set(pub_index[key])))

with open(out_file,'w') as f:
  f.write(json.dumps(tag_index)+'\n')
  f.write(json.dumps(name_index)+'\n')
  f.write(json.dumps(dev_index)+'\n')
  f.write(json.dumps(pub_index)+'\n')
  '''
'''
print(tag_index) 
print(name_index) 
print(dev_index) 
print(pub_index) 
print(products[index[ps.stem("actions")][5]])
'''
