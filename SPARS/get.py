from main import app
from flask import jsonify, session, request
import SPARS as sp
import SPARSusers as spu

@app.route('/get/user')
def getUser():
  return jsonify({"username":session["username"],"name":session["name"],"new":session['new']})
  

@app.route('/get/similar',methods=['POST'])
def getSimilar():
  spars_id = request.form.get('id')
  up = spu.getUserProfile(session['userid'])
  
  gt = sp.getTags(spars_id)
  ui = up['interests'].intersection(gt)  
  sim_ids = sp.getSimilarIDs(spars_id)
  
  max_score = 0
  sg = []
  for i in sim_ids:
    try:
      tags = sp.getTags(i[0])
      s =len(tags.intersection(ui))/len(tags)
      sg.append((i[0],s))
    except:
      pass
  sg.sort(key = lambda x:x[1], reverse=True)
  prod = sp.getAllProductsFromIDs([x[0] for x in sg])
  return jsonify(prod)
  
@app.route('/get/lastSuggestion', methods=['GET'])
def getLastSuggestion():
   up = spu.getUserProfile(session['userid'])
   if len(up['searches'])==0:
    return "0"
   return jsonify(sp.getProductFromID(up['searches'][0]))
   
@app.route('/get/recos', methods=['GET'])
def getRecos():
  up = spu.getUserProfile(session['userid'])
  spars_ids = [x for x in sp.searchIDsByTags(up['interests']) if x not in up['products'] and x not in up['searches']]
  prods = sp.getAllProductsFromIDs(spars_ids)
  return jsonify(prods)
   
