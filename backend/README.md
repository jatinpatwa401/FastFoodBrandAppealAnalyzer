# **Fast Food Brand Appeal**
## Backend Documentation

## `Requirements`

### Setting up the Twitter Crawler

Create a Twitter Developer app to get access to your Consumer API Keys and Access Tokens: https://developer.twitter.com/en/apps <br>
**Note:** You will need to create a Twitter Developer account if you do not have one.

Navigate to the src directory in the cloned repository in your terminal. 
```
cd FastFoodBrandAppeal/src/
```

Create a new file called TwitterConfig.py and add the following information:
```
twitter = {'conKey': '[Insert your public consumer API key]',
           'conSecret': '[Insert your secret consumer API key]',
           'accessToken': '[Insert your public access token]',
           'accessSecret': '[Insert your secret access token]'}
```

Install Twython through pip(Python 2) or pip3(Python3):
```
pip3 install twython
```

## `How to Run`

### Running the Twitter Crawler

Navigate to the src directory in the cloned repository in your terminal. 
```
cd FastFoodBrandAppeal/src/
```

Run the following command(Use "python" instead of "python3" if you are on Python version 2):
```
python3 TwitterCrawler.py
```