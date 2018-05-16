import MySQLdb
import json

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
with open('prod_index.dat') as f:
  print('tags')
  tags = json.loads(f.readline())
  for key in tags:
      for i in range(len(tags[key])):
        tags[key][i]+=1
        c.execute("INSERT into tag_index VALUES('{}', {})".format(key,tags[key][i]))
      #conn.commit()
      c.execute("INSERT into tag_keys VALUES('{}')".format(key))
  conn.commit()
  
  tags = json.loads(f.readline())
  print('names')
  for key in tags:
      for i in range(len(tags[key])):
        tags[key][i]+=1
        c.execute("INSERT into name_index VALUES('{}', {})".format(key,tags[key][i]))
        #conn.commit() 
      c.execute("INSERT into name_keys VALUES('{}')".format(key))
  conn.commit()
  
  tags = json.loads(f.readline())
  print('devs')
  for key in tags:
      for i in range(len(tags[key])):
        tags[key][i]+=1
        c.execute("INSERT into dev_index VALUES('{}', {})".format(key,tags[key][i]))
      c.execute("INSERT into dev_keys VALUES('{}')".format(key))
  conn.commit()    
  
  tags = json.loads(f.readline())
  print('pubs')
  for key in tags:
      for i in range(len(tags[key])):
        tags[key][i]+=1
        c.execute("INSERT into pub_index VALUES('{}', {})".format(key,tags[key][i]))
      c.execute("INSERT into pub_keys VALUES('{}')".format(key))
      
  conn.commit()
