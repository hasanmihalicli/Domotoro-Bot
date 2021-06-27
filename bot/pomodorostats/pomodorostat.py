import os
import json




stat_source = "stats/pomodorouser.json"

#pomodoro update data
async def update_data(users,user):
  user1 = str(user.id)
  if not user1 in users:
    users[str(user.id)] = {}
    users[str(user.id)]['Pomodoro_Count'] = 0
    users[str(user.id)]['money'] = 100
    users[str(user.id)]['word'] = 0
    users[str(user.id)]['pomodoro_message_id'] = None


# pomodoro add point
async def add_xp(users,user,number):
  users[str(user.id)]['Pomodoro_Count'] += number


#set key data
async def set_key(users,user,key,value):
  users[str(user.id)][key] = value



# pomodoro add money
async def add_money(users,user,number):
  users[str(user.id)]['money'] += number

# pomodoro reduce money
async def reduce_money(users,user,number):
  users[str(user.id)]['money'] -= number




# pomodoro add item
async def add_item(users,user,number,item):
  users[str(user.id)][item] += number

# pomodoro reduce item
async def reduce_item(users,user,number,item):
  users[str(user.id)][item] -= number



#get pomodoro count
def get_key(user,key):
  userID = str(user.id)
  if os.path.isfile(stat_source):
    with open(stat_source) as fp :
      myUser = json.load(fp)
    if userID in myUser:
      try:
        return myUser[str(user.id)][key]

      except KeyError:
        return None
    else:
      return None
  else:
    return None


#get item
def get_item(user,item):
  userID = str(user.id)
  if os.path.isfile(stat_source):
    with open(stat_source) as fp :
      myUser = json.load(fp)
    if userID in myUser:
      try:
        return myUser[str(user.id)][item]

      except KeyError:
        return None
    else:
      return None
  else:
    return None

