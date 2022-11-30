#websocket for uptimerobot to ping, keeps bot online
from flask import Flask
from threading import Thread
import random
import os


app = Flask('')

@app.route('/')
def home():
	return 'I am New Light#1249, This WebServer Is Online!'

def run():
  app.run(
    host='0.0.0.0',
		port=8080
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()