from flask import Flask
from threading import Thread

app = Flask('')
data = {}

@app.route('/')
def home():
    return "Hello. I am alive but dead!"

def run():
  app.run(host='0.0.0.0',port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()