import json

file_name="products_all.jl"
out_file = "prod_meta.dat"

m_genres = set()
m_specs = set()
m_tags = set()
m_devs = set()
m_pubs = set()
m_names = set()
m_ids = set()
m_cols = set()

with open(file_name) as f:
  for line in f:
    jobj = json.loads(line)
    m_cols.update(jobj.keys())
    try:
      m_genres.update(jobj['genres'])
    except:
      pass
    try:
      m_specs.update(jobj['specs'])
    except:
      pass
    try:
      m_tags.update(jobj['tags'])
    except:
      pass
    try:
      m_devs.add(jobj['developer'])
    except:
      pass
    try:
      m_pubs.add(jobj['publisher'])
    except:
      pass
    try:
      m_names.add(jobj['app_name'])
    except:
      pass
    try:
      m_ids.add(jobj['id'])
    except:
      pass

#print(m_cols)
print(m_genres)
#print(m_specs)
#print(m_tags)
#print(m_pubs)
#print(m_devs)
#print(m_names)
#print(m_ids)
    
    
