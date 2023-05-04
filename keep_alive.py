#websocket for uptimerobot to ping, keeps bot online
from flask import Flask, render_template, request
from threading import Thread
import random
from json import loads, dumps
import os
import asyncio
import lists

app = Flask(__name__)
app.config.update(
    #TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/datafiles/<string:file>/<string:passkey>')
def jsondat(file,passkey=0):
  if passkey==str(os.environ['WEBPASS']):
    return loads(open(f'{file}.json', 'r').read())
  else:
    return "Access to NEW LIGHT DATA FILES is restricted."

@app.route("/", methods=["POST"])
def get_provider():
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
    return render_template('index.html')
  else:
    return render_template('index.html')
  
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