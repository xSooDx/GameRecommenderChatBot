from SPARSutil import *

def testCredentials(username,password):
  query = "select * from user where username = '{}' and password = '{}'"
  c,conn = connectDB()
  c.execute(query.format(username,password))
  res = False
  msg = "Invlaid Credentials"
  t = c.fetchone()
  if not t == None:
    res =  True
    msg = t
  closeDB(c,conn)
  return res, msg

def registerUser(username, password, name):
  
  query = "select * from user where username = '{}'"
  c,conn = connectDB()
  c.execute(query.format(username))

  if c.fetchone() == None:
    iquery = "INSERT into user (username, password, name) VALUES ('{}','{}','{}')".format(username, password, name)
    try:
      c.execute(iquery)
      conn.commit()
      closeDB(c,conn)
      return True, 'New User Created'
    except Exception as e:
      closeDB(c,conn)
      return False, str(e)    
    
  else: 
    closeDB(c,conn)
    return False, "Username already exists"
  
def addUserInterest(userID, interest):
  query = "insert into user_interests VALUES({},'{}')".format(userID,interest);
  try:
    c,conn = connectDB()
    c.execute(query)    
    conn.commit()
    closeDB(c,conn)
    return True, 'Interest Added'
  except Exception as e:
    return False, str(e)


def addUserSearch(userID, search):
  query = "insert into user_searches(user_id, spars_id) VALUES({},{})".format(userID,search);
  try:
    c,conn = connectDB()
    c.execute(query)    
    conn.commit()
    closeDB(c,conn)
    return True, 'Search Added'
  except Exception as e:
    return False, str(e)
  
  
def addUserProduct(userID, productID):
  query = "insert into user_products(user_id, spars_id) VALUES({},{})".format(userID,productID);
  try:
    c,conn = connectDB()
    c.execute(query)
    conn.commit()
    closeDB(c,conn)
    return True, 'Interest Added'
  except Exception as e:
    return False, str(e)
      

def getUserProfile(userID):
  qp="select spars_id,rating from user_products where user_id = {} LIMIT 15" 
  qi="select interest from user_interests where user_id = {} LIMIT 3"
  qs="select spars_id from user_searches where user_id = {} order by timestamp desc LIMIT 3 "
  
  c,conn = connectDB()
  
  c.execute(qp.format(userID))
  res = c.fetchall()
  prods = set([ (i['spars_id'],i['rating']) for i in res])
  
  
  c.execute(qs.format(userID))
  res = c.fetchall()
  searches = [ i['spars_id'] for i in res]
  
  c.execute(qi.format(userID))
  res = c.fetchall()
  interests = set([ i['interest'] for i in res])
  
  closeDB(c,conn)
  
  return {'user_id':userID, 'products':prods,'interests':interests, 'searches':searches}
  
  
def makeUserOld(userID):
  c,conn = connectDB()
  c.execute("Update user set new=0 where user_id = {}".format(userID))
  conn.commit()
  closeDB(c,conn)

def measureUserSimilarity(userp1, userp2):
  pscore = len(userp1['products'].intersection(userp2['products']))/max(len(userp1['products']),len(userp2['products']))
  #sscore = len(userp1['searches'].intersection(userp2['searches']))/max(len(userp1['searches']),len(userp2['searches']))
  iscore = len(userp1['interests'].intersection(userp2['interests']))/max(len(userp1['interests']),len(userp2['interests']))
  
  return pscore, sscore, iscore


  
