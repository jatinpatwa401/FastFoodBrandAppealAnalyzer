import json
import TwitterConfig as config
from twython import Twython, TwythonStreamer, TwythonError

CONSUMER_KEY = config.twitter['conKey']
CONSUMER_SECRET = config.twitter['conSecret']
ACCESS_TOKEN = config.twitter['accessToken']
ACCESS_SECRET = config.twitter['accessSecret']
    
twitter = Twython (
  CONSUMER_KEY,
  CONSUMER_SECRET,
  ACCESS_TOKEN,
  ACCESS_SECRET
  )


f= open("data.json","a+")

class MyStreamer(TwythonStreamer):
  def on_success(self, data):
    if ('place' in data and data['place'] is not None) or ('location' in data['user'] and data['user']['location'] is not None):
      print('Collecting data')
      f.write(json.dumps(data) + ',\n')
      # f.write(str(data['user']['location']))
      # f.write('\n')

  def on_error(self, status_code, data):
    print(status_code)
    # self.disconnect()

# List of Top 50 Fast Food Brands in the US
brands = 'McDonald\'s,McDonalds,Starbucks,Subway,Taco Bell,Chick-fil-A,Chick fil A,Wendy\'s,Wendys,Burger King,Dunkin\',Dunkin\' Donuts,Dunkin Donuts,Domino\'s,Dominos,Panera,Panera Bread,Pizza Hut,Chipotle,Sonic Drive-In,Sonic Drive In,KFC,Kentucky Fried Chicken,Arby\'s,Arbys,Little Caesars,Dairy Queen,DQ,Jack in the Box,Panda Express,Popeye\'s,Popeyes,Papa John\'s,Papa Johns,Whataburger,Jimmy John\'s,Jimmy Johns,Hardee\'s,Hardees,Zaxby\'s,Zaxbys,Five Guys,Culver\'s,Culvers,Carl\'s Jr,Carl\'s Junior,Carl\'s Jr.,Carls Jr,Carls Junior,Carls Jr.,Bojangles\',Bojangles,Wingstop,Raising Cane\'s,Raising Canes,Jersey Mike\'s,Jersey Mikes,Steak \'n\'n Shake,Steak \'n Shake,Stake n Shake,In-N-Out,In-N-Out Burger,In \'N Out,In \'N Out Burger,In N Out,In N Out Burger,El Pollo Loco,Qdoba,Checkers,Rally\'s,Rallys,Del Taco,Firehouse Subs,Papa Murphy\'s,Papa Murphys,Tim Hortons,Church\'s Chicken,Churchs Chicken,Moe\'s,Moes,McAlister\'s Deli,McAlisters Deli,Jason\'s Deli,Jasons Deli,Marco\'s Pizza,Marcos Pizza,Baskin-Robbins,Baskin Robbins,Auntie Anne\'s,Auntie Annes,Boston Market,White Castle'

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
for i in range(10):
  stream.statuses.filter(track=brands)