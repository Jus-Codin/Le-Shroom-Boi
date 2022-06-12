import json

global server_id
global current_count
global timestamp
global data

def read_data():
  data = json.load(open("data.json", 'r'))
  return data

def write_data(current_count, timestamp):
  data = {
    "Server ID": {
      "Current count": current_count, 
      "Timestamp": timestamp
    }
  }
  json.dump(data, open("data.json", "w"), indent=4)
