# **Backend Documentation**

## Requirements

Install Python 3 by following the documentation at https://www.python.org/downloads/

Install pip3 by running the following commands in your terminal:
```
sudo apt update
sudo apt install python3-pip
pip3 --version
```

Install Spark by following the documentation at https://spark.apache.org/docs/latest/index.html </br>
Set up the Spark Standalone Mode if you do not have access to a cluster.

Install Twython through your terminal using pip3:
```
pip3 install twython
```

Install MySQL by following the documentation at https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/ </br>
I recommend installing the MySQL Workbench as it is easier to use than the terminal.

### `Setting up the Twitter Crawler`

Create a Twitter Developer app to get access to your Consumer API Keys and Access Tokens: https://developer.twitter.com/en/apps <br>
**Note:** You will need to create a Twitter Developer account if you do not have one.

Navigate to the collection directory in your terminal:
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

Navigate to the MLModels directory in your terminal:
```
cd FastFoodBrandAppeal/backend/classification/MLModels
```

Download the sentiment training dataset: training.1600000.processed.noemoticon.csv
</br> https://www.kaggle.com/kazanova/sentiment140
</br> Save this file in the MLModels directory

Download the sarcasm training dataset: train-balanced-sarcasm.csv
</br> https://www.kaggle.com/danofer/sarcasm
</br> Save this file in the MLModels directory

Create the sentiment and sarcasm machine learning models: </br>
```
spark-submit sentimentTest.py
spark-submit sarcasmTest.py
```

### `Pre-processing the Labeled Data`

Navigate to the processing directory in your terminal:
```
cd FastFoodBrandAppeal/backend/processing
```

Run the following command to pre-process the data:
```
python3 preProcessing.py
```
This will convert all locations to state and country names and abbreviations.

## How to Run

### `Running the Twitter Crawler`

Navigate to the src directory in the cloned repository in your terminal:
```
cd FastFoodBrandAppeal/src/
```

Run the following command to start the crawler:
```
python3 TwitterCrawler.py
```

### `Running the ML Classifier Models`

Navigate to the classification directory in your terminal:
```
cd FastFoodBrandAppeal/backend/classification
```

Run the following command to label your data found in /backend/data/rawData.json and convert it to a series of csv files:
```
spark-submit cleanJsonTweets.py
```

Navigate to the data directory in your terminal:
```
cd FastFoodBrandAppeal/backend/data/
```

Consolidate all of the csv files into one csv:
```
cat csvFiles/*.csv > labeledData.csv
```

### `Processing the Data into Meaningful Data`

Navigate to the processing directory in your terminal:
```
cd FastFoodBrandAppeal/backend/processing
```

Run the following command to aggregate the results:
```
spark-submit sparkProcessing.py
```
This will count the unique occurences of each (restaurant, location, sentiment, sarcasm) tuple and leave the data in this form: </br>
restaurant | location | numPosSentiment | numNegSentiment | numPosSarcasm | numNegSarcasm

## Populate the Database

* Open the MySQL Workbench, or open MySQL through the terminal. </br>
* Create and configure a new database called cs226. </br>
* Connect to the database and start the database server on localhost. </br>
* Import /backend/data/completedProcessing.csv as a new table. </br>
*If you are using the MySQL Workbench, right click on "Tables" and run the "Table Data Import Wizard"*</br>

Now create a Dump.sql file to be placed in frontend/visualisation/database.
* In the MySQL Workbench, go to Server > Data Export
* Select the cs226 database schema and the table you created inside of it.
* Change the export path to YourPath/FastFoodBrandAppeal/frontend/visualisation/database/Dump.sql
*Note: This file already exists as Dump20191204.sql so you can run the frontend for demo purposes*

Congratulations! Your backend is completely setup and ready to be called by the frontend code.