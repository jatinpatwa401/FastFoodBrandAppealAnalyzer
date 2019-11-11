# **Fast Food Brand Appeal**
## Using Twitter and Sentiment Analysis 

## `Authors`

Anish Sekar </br>
Brandon Herrera </br>
Justin Schopick </br>
Yogesh Singh

## `Overview`

This project applies sentiment analysis to a large amount of tweets to determine the appeal of Fast Food chains in the United States.

**The Goal:**
* Better understand fast food chains’ brand appeal in the United States. 
* Twitter has over 300 million monthly active users as of 2019
* Many post about their opinions on a variety of different topics, so there is a vast amount of data related to fast food.

**The Benefit:**
* By using sentiment analysis to determine if a tweet is positive or negative, along with geolocation data, we can visualize the public appeal of fast food chains in different areas of the United States.

## `Technologies Used`

### **Languages and Frameworks**

Python: A high-level programming language. </br> https://www.python.org/

### **Application Programming Interfaces**

Twython: Actively maintained, pure Python wrapper for the Twitter API. </br> https://developer.twitter.com/en/docs/developer-utilities/twitter-libraries

## `Prerequisites`

### Cloning this Repository

Navigate to the desired location on your computer. Enter the following command in your terminal:
```
git clone https://github.com/jschopick/FastFoodBrandAppeal.git
```

### Requirements for Twitter Crawler

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

### Starting the Twitter Crawler

Navigate to the src directory in the cloned repository in your terminal. 
```
cd FastFoodBrandAppeal/src/
```

Run the following command(Use "python" instead of "python3" if you are on Python version 2):
```
python3 TwitterCrawler.py
```

## `License`

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.