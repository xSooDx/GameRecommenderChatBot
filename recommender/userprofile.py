import search
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

products, similarity, tag_index, name_index, dev_index, pub_index = search.loadProdata(prod_file,sim_file)

userprofile = []

def recommend():
  pass

while True:
  a = input().split()
  if a[0]=='recommend':
    recommend()
  elif a
  
  

