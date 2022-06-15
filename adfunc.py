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

def write_data(current_count, timestamp):
  data = {
    "Server ID": {
      "Current count": current_count, 
      "Timestamp": timestamp
    }
  }
  json.dump(data, open("data.json", "w"), indent=4)


def crash_check(current_count, timestamp):
  precrash_data = read_data()
  last_count = precrash_data["Current count"]
  last_ctime = precrash_data["Timestamp"]
  last_ts = print(time.mktime(datetime.datetime.strptime(last_ctime, "%Y/%m/%d %H:%M:%S").timetuple()))
  new_day = last_ts.strfttime("%d")
  current_day = timestamp.strfttime("%d")
  if new_day != current_day:
    return last_count
  else:
    last_count = 0
    return last_count