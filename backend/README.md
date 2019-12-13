# **Backend Documentation**

## Requirements

Install Python 3 by following the documentation at https://www.python.org/downloads/

Install pip3 by running the following commands in your terminal.
```
sudo apt update
sudo apt install python3-pip
pip3 --version
```

Install Spark by following the documentation at https://spark.apache.org/docs/latest/index.html </br>
Set up the Spark Standalone Mode if you do not have access to a cluster.

Install Twython through your terminal using pip3(Python3):
```
pip3 install twython
```

### `Setting up the Twitter Crawler`

Create a Twitter Developer app to get access to your Consumer API Keys and Access Tokens: https://developer.twitter.com/en/apps <br>
**Note:** You will need to create a Twitter Developer account if you do not have one.

Navigate to the collection directory in your terminal. 
```
cd FastFoodBrandAppeal/backend/collection/
```

Create a new file called TwitterConfig.py and add the following information:
```
twitter = {'conKey': '[Insert your public consumer API key]',
           'conSecret': '[Insert your secret consumer API key]',
           'accessToken': '[Insert your public access token]',
           'accessSecret': '[Insert your secret access token]'}
```

### `Setting up the Sentiment & Sarcasm Classifiers`

Navigate to the MLModels directory in your terminal. 
```
cd FastFoodBrandAppeal/backend/classification/MLModels
```

Download the sentiment training dataset: training.1600000.processed.noemoticon.csv
</br> https://www.kaggle.com/kazanova/sentiment140
</br> Save this file in the MLModels directory

Download the sarcasm training dataset: train-balanced-sarcasm.csv
</br> https://www.kaggle.com/danofer/sarcasm
</br> Save this file in the MLModels directory

Now create the sentiment and sarcasm machine learning models: </br>
```
spark-submit sentimentTest.py
spark-submit sarcasmTest.py
```

## How to Run

### `Running the Twitter Crawler`

Navigate to the src directory in the cloned repository in your terminal. 
```
cd FastFoodBrandAppeal/src/
```

Run the following command to start the crawler:
```
python3 TwitterCrawler.py
```

### `Running the ML Classifier Models`

Navigate to the classification directory in your terminal. 
```
cd FastFoodBrandAppeal/backend/classification
```

Run the following command to label your data found in /backend/data/rawData.json and convert it to a series of csv files:
```
spark-submit cleanJsonTweets.py
```

Navigate to the data directory in your terminal. 
```
cd FastFoodBrandAppeal/backend/data/
```

Consolidate all of the csv files into one csv:
```
cat csvFiles/*.csv > labeledData.csv
```