import json
import numpy as np
from functools import reduce

file_name="products_all.jl"
out_file="prod_similar.dat"
max_sim = 5

'''
  Get Similarity Between
'''
def getSimilarity(a,b):
  tscore = 0
  gscore = 0
  sscore = 0
  mp=0
  try:
    for i in a['tags']:
      if i in b['tags']:
        tscore+=1
    mp += max(len(a['tags']),len(b['tags']))
  except: pass
  try:
    for i in a['genres']:
      if i in b['genres']:
        gscore+=1
    mp += max(len(a['genres']),len(b['genres']))
  except: pass
  try:
    for i in a['specs']:
      if i in b['specs']:
       sscore+=1
    sscore*=0.5
    mp += max(len(a['specs']),len(b['specs']))*0.5
  except: pass
  if mp==0: return 0
  sim = tscore+gscore+sscore 
  
  return sim/mp
  
def findMin(a):
  mi = 0
  m = a[0]
  for i in range(1,len(a)):
    if a[i][1]<a[mi][1]:
      mi = i
      m=a[i]
  return (m,mi)

'''
  Add similar products to similar list
'''
def addSimilar(a,i,s):
  sim = a['similar']
  lsim = len(sim)
  if lsim >= 10:
    if s>a['min'][1]:
      sim[a['min'][2]] = (i,s)
      p,q = findMin(sim)
      a['min'] = (p[0],p[1],q)
  else:
    sim.append((i,s))
    if 'min' in a :
      if s<a['min'][1]:
        a['min'] = (i,s,lsim)
    else:
      a['min'] = (i,s,lsim)

products = []
num = 0
with open(file_name) as f:
  for line in f:
    jobj = json.loads(line)
    products.append(jobj)
    num+=1
    #if num == 100: break
    if num % 10 == 0: print("entry", num)
    '''jobj['similar'] = []
    for i in range(num):
      s = getSimilarity(products[i],jobj)
      addSimilar(products[i],num,s)
      addSimilar(jobj,i,s)
    products.append(jobj)
    num+=1
    #if num == 100: break
    if num % 10 == 0: print("entry", num)
with open(out_file,"w") as f:
  for p in products:
    s = json.dumps(p["similar"])
    f.write(s+"\n")
    
#print(products)
'''
print (getSimilarity(products[0],products[10365]))

  
