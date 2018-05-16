from main import app
from flask import jsonify, session, request
import SPARSusers as spu
import SPARSutil as util
import SPARS as sp


@app.route("/store/tags", methods=['POST'])
def storeTags():
  interests = util.remStopWords(util.splitStem(request.form.get('data')))
  for i in interests:
    spu.addUserInterest(session['userid'],i)
  return "Done"
    
@app.route("/store/game", methods=['POST'])
def storeGame():
  spars_id, game = sp.matchName(request.form.get('data'))
  if spars_id==None:
    return '0'
  spu.addUserProduct(session['userid'],spars_id)
  if session['new'] ==1:
    session['new'] = 0
    spu.makeUserOld(session['userid'])
  rating = sp.getProductRating(spars_id)
  
  return jsonify({'name':game,'spars_id':spars_id,'rating':rating})
  
@app.route("/store/search", methods=['POST'])
def storeSearch():
  spars_id = request.form.get('data')
  r,m = spu.addUserSearch(session['userid'],spars_id)
  print(m)
  return str(r)
  
