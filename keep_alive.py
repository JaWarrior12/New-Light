#websocket for uptimerobot to ping, keeps bot online
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
#from flask_ipban import IpBan
from wtforms import RadioField
from threading import Thread
import random
from json import loads, dumps
import os
import asyncio
import lists

app = Flask(__name__)
seckey = os.urandom(32)
app.config.update(
    #TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=seckey
)
#ip_ban=IpBan(app)
#ip_ban = IpBan(ban_seconds=200)

class SimpleForm(FlaskForm):
  def setchoices():
    opts=[]
    data=lists.readdataE()
    for x in data:
      if x=="ban" or x=="banguilds":
        continue
      else:
        #print(x)
        name=str(data[x]["name"])
        pingchan=str(x)
        obj=tuple((pingchan,name))
        opts.append(obj)
        #print(opts)
    return opts
  clan = RadioField('btn', choices=setchoices(),default=1, coerce=int)

@app.route('/')
def home():
  form = SimpleForm()
  return render_template('index.html',form=form)

@app.route('/datafiles/<string:file>/<string:passkey>')
def jsondat(file,passkey=0):
  if passkey==str(os.environ['WEBPASS']):
    return loads(open(f'{file}.json', 'r').read())
  else:
    return "Access to NEW LIGHT DATA FILES is restricted."

@app.route("/", methods=["POST"])
def get_provider():
  #print(form.clan.data)
  rf = request.form['btn']
  if rf =="index":
    dp = request.form["provider"]
    dpb = request.form["clan"]
    #dp_lower_case #= dp.lower()
    #print(f'{dp}')
    data = lists.readother()
    format=[dpb,dp]
    #print(data)
    data["pinglinks"].append(format)
    #print(data)
    lists.setother(data)
    return render_template('submit.html')
  elif rf=="submit":
    form = SimpleForm()
    return render_template('index.html',form=form)
  else:
    form = SimpleForm()
    return render_template('index.html',form=form)
  
def run():
  app.run(
    host='0.0.0.0',
		port=8080
	)

def keep_alives():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()