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
with open('prod_similar.dat') as f:
  for line in f:
      d = json.loads(line)
      print(d)
      for i in d:
        i[0] +=1
      print(d)
      
      c.execute("INSERT into similar (similar) VALUES('"+str(d)+"')")
      
conn.commit()
