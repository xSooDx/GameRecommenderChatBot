from main import app
from flask import render_template, request, redirect, url_for, session, flash
import SPARS as sp
import SPARSusers as spu
from functools import wraps

@app.route("/bot")
def bot():
  if not 'userid' in session:
    return redirect(url_for('home'))
  return render_template("bot.html")
  
@app.route("/home")
@app.route("/")
def home():
  return render_template("index.html")
  
  
@app.route("/login", methods=["POST"])
def login():
  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')
    r,m = spu.testCredentials(username,password)
    if r:
      session['userid'] = m['user_id']
      session['username'] = username
      session['name'] = m['name']
      session['new'] = m['new']
      return redirect(url_for("bot"))
    else:
      flash(m)
      return redirect(url_for("home"))
    
  
@app.route("/register", methods=["POST"])
def register():
  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    r,m = spu.registerUser(username,password,name)
    if r:
      r,m = spu.testCredentials(username,password)
      session['userid'] = m['user_id']
      session['username'] = username
      session['name'] = name
      session['new'] = 1
      return redirect(url_for("bot"))
    else:
      flash(m)
      return redirect(url_for("home"))
      
      
      
