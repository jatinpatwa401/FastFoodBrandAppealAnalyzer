# **Fast Food Brand Appeal**
## Using Twitter and Sentiment Analysis 

## `Authors`

Anish Sekar </br>
Brandon Herrera </br>
Justin Schopick </br>
Yogesh Singh

## `Overview`

This project applies sentiment analysis to 

**The Goal:**
* Determine what genres are most preferred in different countries around the world by finding the location of users on Twitter that follow music artists.

**The Benefit:**
* World Music can reveal the regular pattern of the primary music preference in different parts of the world. This can help music providers provide and suggest music to the users in different regions and supply data support to anthropological and sociological studies.

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