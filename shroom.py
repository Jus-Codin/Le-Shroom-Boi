
import json
from typing import TypedDict


class UserDict(TypedDict):
  farmed: int

class ShroomDict(TypedDict):
  server_id: int
  shroom_count: int
  updated: int
  users: dict[int, UserDict]

class ShroomFarm:
  def __init__(self, fp: str = "data.json"):
    self.fp = fp
    self.data = self._load_data()

  def _load_data(self) -> ShroomDict:
    with open(self.fp, "r") as f:
      data = json.load(f)
    return data
    
  def _save_data(self):
    with open(self.fp, "w") as f:
      json.dump(self.data, f)

  def __getattr__(self, attr) -> int | dict[int, UserDict]:
    attr = self.data.get(attr)
    if attr is None:
      raise AttributeError
    else:
      return attr

  def get_user(self, user_id: int) -> UserDict | None:
    return self.users.get(user_id)

  def create_user(self, user_id: int):
    if self.get_user(user_id) is not None:
      raise ValueError(f"user with ID `{user_id}` already exists")
    self.users[user_id] = {"farmed": 0}

  def update_user(self, user_id: int, d: UserDict):
    if self.get_user(user_id) is None:
      raise ValueError(f"user with ID `{user_id}` does not exist")
    self.users[user_id] = d

  