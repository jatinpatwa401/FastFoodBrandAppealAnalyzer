import TwitterConfig as config
from twython import Twython, TwythonError

print(config.twitter['conKey'])
print(config.twitter['conSecret'])
print(config.twitter['accessToken'])
print(config.twitter['accessSecret'])