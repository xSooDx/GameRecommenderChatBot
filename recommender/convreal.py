import json
from pprint import pprint
import sys
import MySQLdb
from MySQLdb import escape_string as thwart
#reload(sys)
#sys.setdefaultencoding('utf-8')
data = []

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
with open('products_all.jl') as data_file:    
    for line in data_file:
      d = json.loads(line)
      data.append(d)
fw = open("check.sql",'w')
#pprint(data[0]["app_name"])
s=0
l=['discount_price', 'specs', 'metascore', 'price', 'title', 'publisher', 'id', 'sentiment', 'developer', 'release_date', 'app_name', 'tags', 'url', 'reviews_url', 'genres']
l2=[0]*30
for i in data:
    cnt=0
    if(s==2):
        break
    else:
        text=""
        text2=""
        for j in l:
            if(j in i):
                text2='"'+str(i[j]).replace('"', '')+'"'
                l2[cnt]=text2
                cnt=cnt+1
            elif(j in i and isinstance(i[j], list)):
                for k in i[j]:
                    text=text+","+k
                text.replace('"', '')
                l2[cnt]='"'+text+'"'
                cnt=cnt+1  
            else:
                l2[cnt]='"none"'
                cnt=cnt+1
            
            
            
        c.execute("INSERT into product(discount_price,specs,metascore,price,title,publisher,id,sentiment,developer,release_date,app_name,tags,url,reviews_url,genres) VALUES("+str(l2[0])+","+str(l2[1])+","+str(l2[2])+","+str(l2[3])+","+str(l2[4])+","+str(l2[5])+","+str(l2[6])+","+str(l2[7])+","+str(l2[8])+","+str(l2[9])+","+str(l2[10])+","+str(l2[11])+","+str(l2[12])+","+str(l2[13])+","+str(l2[14])+")")

        
conn.commit()
        
    
	
