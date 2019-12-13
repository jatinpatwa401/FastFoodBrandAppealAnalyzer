from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row

# For creating a data frame in spark
from pyspark.ml import Pipeline

# For Naive Bayes classifier
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel, LogisticRegression, LogisticRegressionModel

# For extracting features 
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer
from pyspark.ml.feature import IndexToString


import shutil
import sys
import string
import json
import re

tweetsDate = "tweets20191121"
path = "./jsonTweets/" + tweetsDate + "*"
#path = "/opt/hadoop/home/hadoop6/bherr006/jsonTweetsHourly/" + tweetsDate + "*"
#tweetsDate = "dataWithLocation2"
#path = "/opt/hadoop/home/hadoop6/bherr006/dataWithLocation2.json"

sc = SparkSession.builder.appName("ProcessData").getOrCreate()        
sc.sparkContext.setLogLevel("Error") # spark context

resturantList = ['jollibee','l&l hawaiian barbecue','manchu wok','noodles & company','panda express','pei wei asian diner','pho hoa','pick up stix','yoshinoya','au bon pain','auntie annes','brueggers bagels','cinnabon','corner bakery cafe','daylight donuts','duck donuts','einstein bros bagels','great american cookies','great harvest bread company','honey dew donuts','insomnia cookies','krispy kreme','le madeleine','le pain quotidien','mrs fields','pretzelmaker','wetzels pretzels','winchells donuts','gold star chili','shanes rib shack','skyline chili','biggby coffee','caribou coffee','the coffee bean & tea leaf','coffee beanery','dunkin donuts','dunn brothers coffee','dutch bros coffee','gloria jeans coffees','jamba juice','juice it up','orange julius','peets coffee','planet smoothie','robeks','smoothie king','starbucks','tim hortons','tropical smoothie cafe','bojangles famous chicken n biscuits','boston market','bushs chicken','chesters international','chickfila','chicken express','churchs chicken','el pollo loco','golden chick','hartz chicken','kfc','lees famous recipe chicken','louisiana famous fried chicken','pollo campero','pollo tropical','popeyes','raising canes chicken fingers','slim chickens','wingstop','zaxbys','zoes kitchen','baskinrobbins','ben & jerrys','braums','carvel','cold stone creamery','dairy queen','fosters freeze','friendlys','graeters','haagendazs','marble slab creamery','menchies frozen yogurt','pinkberry','ritas italian ice','sweet frog','tcby','tutti frutti frozen yogurt','yogurtland','a&w restaurants','arctic circle restaurants','back yard burgers','big boy','blakes lotaburger','burgerfi','burger king','carls jr','checkers','cook out','culvers','farmer boys','fatburger','five guys','freddys frozen custard & steakburgers','frischs big boy','fuddruckers','the habit burger grill','hwy 55 burgers shakes & fries','innout burger','jack in the box','krystal','mcdonalds','milos hamburgers','mooyah','shake shack','smashburger','sonic drivein','steak n shake','wayback burgers','wendys','whataburger','white castle','hot dog on a stick','portillos restaurants','wienerschnitzel','baja fresh','cafe rio','california tortilla','chipotle mexican grill','del taco','freebirds world burrito','fuzzys taco shop','moes southwest grill','qdoba','rubios coastal grill','salsaritas fresh mexican grill','taco bell','taco bueno','taco cabana','taco del mar','taco johns','taco time','tijuana flats','americas incredible pizza company','blaze pizza','cicis','dominos','donatos pizza','east of chicago pizza','fazolis','foxs pizza den','gattis pizza','giordanos pizzeria','godfathers pizza','happys pizza','hungry howies pizza','jets pizza','little caesars','marcos pizza','mod pizza','papa ginos','papa johns pizza','papa murphys','pieology pizzeria','pizza hut','pizza inn','pizza ranch','sbarro','villa italian kitchen','saladworks','sweetgreen','arbys','blimpie','camilles sidewalk cafe','capriottis','charleys philly steaks','cosi','dangelo grilled sandwiches','firehouse subs','great wraps','jasons deli','jersey mikes subs','jimmy johns','lees sandwiches','lennys grill & sub','mcalisters deli','newks eatery','panera bread','penn station east coast subs','pita pit','port of subs','potbelly sandwich shop','pret a manger','primo hoagies','quiznos','sandellas flatbread cafe','schlotzskys','steak escape','subway','togos','which wich','captain ds','long john silvers','applebees','beef obradys','bjs restaurant','black bear diner','bob evans restaurant','boomerang diner','cheddars scratch kitchen','the cheesecake factory','golden corral','hard rock cafe','hooters','houlihans','huddle house','johnny rockets','lubys','ocharleys','ruby tuesday','sharis cafe & pies','souplantation','tgi fridays','twin peaks','village inn','yard house','benihana','huhot mongolian grill','pf changs china bistro','bar louie','millers ale house','dennys','first watch','ihop','the original pancake house','perkins restaurant and bakery','waffle house','buffalo wild wings','hooters','hurricane grill & wings','the melting pot','mimis cafe','max & ermas','red robin','chilis','chuys','on the border mexican grill & cantina','brio tuscan grill','buca di beppo','california pizza kitchen','carinos italian','carrabbas italian grill','maggianos little italy','olive garden','romanos macaroni grill','happy joes','mellow mushroom','old chicago pizza & taproom','rosatis authentic chicago pizza','round table pizza','shakeys pizza','bonefish grill','red lobster','cracker barrel','dickeys barbecue pit','famous daves','smokey bones','sonnys bbq','the capital grille','flemings prime steakhouse & wine bar','fogo de chao','logans roadhouse','longhorn steakhouse','mortons the steakhouse','outback steakhouse','ruths chris steak house','saltgrass steak house','texas roadhouse','tony romas','sizzler','western sizzlin','chuck e cheeses','dave & busters','peter piper pizza', 'jack', 'jacks']


def removeComma(x):
   if(x[len(x) - 1] == ','):
      return x[:-1]
   return x

def checkEmpty(x):
    if (x == ""):
        return False
    return True

def getMatch(x):
    if(len(x) == 0):
        return "unknown"
    for resturant in resturantList:
        if(re.search(r"\b" + re.escape(resturant) + r"\b", x)):
            return resturant
    return "unknown"

def getText(x):
   coorList = []
   tempList = []
   hashtagList = []
   mentionList = []
   jsonTweet = json.loads(x)

   tweetText = jsonTweet['text'].encode('utf-8')
   tweetText = re.sub(r'[^\x00-\x7F]+','', tweetText)
   tweetText = re.sub(r'[\n\t\r,#@"\'|\-\\]', "", tweetText)
   if (not(checkEmpty(tweetText))):
      return tempList.append("") 
   tweetText = tweetText.lower()
   
   if (jsonTweet['is_quote_status'] == True):
      if ('quoted_status' in jsonTweet):
         reply = True
         replyText = jsonTweet['quoted_status']['text'].encode('utf-8')
         replyText = re.sub(r'[^\x00-\x7F]+','', replyText)
         replyText = re.sub(r'[\n\t\r,#@"\'|\-\\]', "", replyText)
         replyText = replyText.lower()
         tweetResturant = getMatch(tweetText + " " + replyText)
      else:
         reply = False
         replyText = "Not in reply."
         tweetResturant = getMatch(tweetText)
   else:
      reply = False
      replyText = "Not in reply."
      tweetResturant = getMatch(tweetText)

   tweetID = jsonTweet['id']
  
   tweetUser = jsonTweet['user']['screen_name'].encode('utf-8')
   tweetUser = re.sub(r'[^\x20-\x7E]+','', tweetUser)
   tweetUser = re.sub(r'[\n\t\r]', '', tweetUser)
   tweetUser = tweetUser.lower()
   
   tweetTimeStamp = jsonTweet['created_at'].encode('utf-8')

   if (not(jsonTweet['coordinates'] == None)):
      tweetGeo = True
      tweetLongitude = jsonTweet['coordinates']['coordinates'][0]
      tweetLatitude = jsonTweet['coordinates']['coordinates'][1]
   else:
      tweetGeo = False
      tweetLongitude = 0.0
      tweetLatitude = 0.0
   
   tweetUrl = "https://twitter.com/" + tweetUser + "/status/" + str(tweetID)
   
   if (jsonTweet['user']['location'] == None):
      tweetLocation = "unknown"
   else:
      tweetLocation = jsonTweet['user']['location']
      tweetLocation = re.sub(r'[^\x20-\x7E]+','', tweetLocation)
      tweetLocation = re.sub(r'[\n\t\r]', '', tweetLocation)

   tempList.append(tweetID)
   tempList.append(tweetUser)
   tempList.append(tweetTimeStamp)
   tempList.append(tweetGeo)
   tempList.append(tweetLongitude)
   tempList.append(tweetLatitude)
   tempList.append(tweetText)
   tempList.append(reply)
   tempList.append(replyText)
   tempList.append(tweetResturant)
   tempList.append(tweetUrl)
   tempList.append(tweetLocation)
   return tempList


lines = sc.read.text(path).rdd.map(lambda x: x[0])\
          .map(lambda x: removeComma(x))\
          .map(lambda x: getText(x))\
          .filter(lambda x: not(x == None))\
          .filter(lambda x: checkEmpty(x[0]))\
          .map(lambda x: Row(id=x[0], user=x[1], timeStamp=x[2], geo=x[3], longitude=x[4], latitude=x[5], text=x[6], reply=x[7], replyText=x[8], resturant=x[9], url=x[10], userLocation=x[11]))


df = sc.createDataFrame(lines)


tokenizer = Tokenizer(inputCol = "text", outputCol = "words")
# Extract the features
hashing_tf = HashingTF(numFeatures = 2**16, inputCol = "words", outputCol = "tf")
idf = IDF(inputCol = "tf", outputCol = "features", minDocFreq = 5)
lines = Pipeline(stages = [tokenizer, hashing_tf, idf])

# Get the data to test
line_fit = lines.fit(df)
test_model = line_fit.transform(df)

# Load the trained model
sentimentModel = LogisticRegressionModel.load("./MLModels/logisticRegressionSentiment")
sarcasmModel =  LogisticRegressionModel.load("./MLModels/logisticRegressionSarcasm")


# apply the models
result = sentimentModel.transform(test_model)
result = result.withColumnRenamed("prediction", "sentimment")
result = result.drop("words", "tf", "features", "rawPrediction", "probability")

line_fit = lines.fit(result)
test_model = line_fit.transform(result)

result = sarcasmModel.transform(test_model)
result = result.withColumnRenamed("prediction", "sarcasm")
result = result.drop("words", "tf", "features", "rawPrediction", "probability")
result.show(10, False)


result.write.csv("./csvTweets/" + tweetsDate)


sc.stop()
