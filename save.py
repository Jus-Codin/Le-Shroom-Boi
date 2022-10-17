import json
import time
from datetime import datetime

global server_id
global current_count
global timestamp
global data



def read_data():
  data = json.load(open("data.json", 'r'))
  return data

def write_data(current_count, timestamp, server_id):
  data = {
    "Save data": {
      "Server ID": server_id, 
      "Current count": current_count, 
      "Timestamp": timestamp
    }
  }
  json.dump(data, open("data.json", "w"), indent=4)
