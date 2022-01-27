# Twitter User Scraper

## Setup Instructions
Before running Twitter User Scraper, the following must be completed:

1. You must create a Twitter Development Account (Which can be created at https://developer.twitter.com/). Make sure to save your bearer token!

2. Add you bearer token as an environment variable on your system with tag BEARER_TOKEN. 

* Instructions for different OS:
   * Mac: https://phoenixnap.com/kb/set-environment-variable-mac
   * Windows: https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0
   * Linux: https://www.cyberciti.biz/faq/set-environment-variable-linux/

3. Open up terminal and navigate into the 'twitter-user-scraper' directory

4. Make sure python is installed. (utilize pyenv install with the version in .python-version)

5. run 'pip install -r requirements.txt' on the terminal

## Functionality
The scraper can be run with 'python twitter_user_scraper_tool.py' and has the following arguments:

Usage: twitter_user_scraper_tool.py [-h] [--input INPUT] [--output OUTPUT] [--followers] [--timeline] [names [names ...]]

Positional arguments:
* names: Twitter usernames to scrape information from

Optional arguments:
* -h, --help : show this help message and exit
* --input INPUT, -i INPUT : input file path (such that each username is on a newline)
* --output OUTPUT, -o OUTPUT : output file path (default: user_information.json)
* --followers, -f : Adds followers statistics to dataset
* --timeline, -t : Adds timeline statistics to dataset

For instance possible inputs might look like the following:
* python twitter_user_scraper_tool.py JoeBiden -f -t
* python twitter_user_scraper_tool.py JoeBiden elonmusk -f 
* python twitter_user_scraper_tool.py -i input.txt -f -t
* python twitter_user_scraper_tool -o thisissoextra.json

The tool works by taking in either a list of names through command line arguments or by a text file (such that each name is on a new line) and sending requests to the Twitter api for each name. By default the program only calls for PII information which looks something like the following:

   
      "User": {
         "name": "Joe Biden",
         "description": "Husband to @DrBiden, proud father and grandfather. Ready to build back better for all Americans. Official account is @POTUS.",
         "created_at": "2007-03-11T17:51:24.000Z",
         "public_metrics": {
               "followers_count": 32252587,
               "following_count": 48,
               "tweet_count": 7936,
               "listed_count": 37956
         },
         "location": "Washington, DC",
         "username": "JoeBiden",
         "id": "939091"
      }


There are options to recieve the other required statistics by using the "--timeline" and "--followers" flags. 

"--followers" adds the "Followers" parameter to the UserData object which contains a list of all followers (up to constants.MAX_FOLLOWERS in constants.py which is preset at 1000) and looks like the following:

      "Followers": [
         {
               "id": "2371101667",
               "name": "andres",
               "username": "felipelargo95"
         },
         {
               "id": "1170596890251071490",
               "name": "JS EC",
               "username": "JSEC87184808"
         },
         {
               "id": "1346605729889865729",
               "name": "Luis Morales ruiz",
               "username": "LuisMoralesrui5"
         }
         ...
      ]

"--timeline" adds the "TweetTimeline" paramater to the UserData object and calculates the top 5 most-retweeted posts, the top 5 most liked posts, the top 5 most retweeted posts that the user retweets and the top 3 most used hashtags and cashtags (if anyone actually uses those?) by the user amongst the last 3200 tweets from the user. An example is as follows:

      "TweetTimeline": {
         "most_retweeted_tweets": [
               {
                  "created_at": "2021-06-01T09:19:57.000Z",
                  "id": "1399656957611552773",
                  "text": "\ud83c\udde7\ud83c\uddf7\ud83c\udf51\ud83c\udf46\ud83c\uddea\ud83c\uddf8 https://t.co/KQSi47Ao8a",
                  "public_metrics": {
                     "retweet_count": 1,
                     "reply_count": 1,
                     "like_count": 8,
                     "quote_count": 0
                  },
                  "entities": {
                     "urls": [
                           {
                              "start": 7,
                              "end": 30,
                              "url": "https://t.co/KQSi47Ao8a",
                              "expanded_url": "https://twitter.com/Richardbi10/status/1399656957611552773/photo/1",
                              "display_url": "pic.twitter.com/KQSi47Ao8a"
                           }
                     ]
                  }
               }
               ...
         ],
         "most_liked_tweets": [
            ...
         ],
         "most_retweeted_retweets": [
            ...
         ],
         "hashtags": [
               [
                  100,
                  "WOW"
               ]
               ...
         ],
         "cashtags": [
            ...
         ]
      }

## Reading json Output Files
Json files can be read using the load_user_json("json file path') method of the UserDataHandler class within user_data_handler.py. This will return a list of UserData objects.

## **Warnings**
- Due to how the Twitter is structured there are caps on various requests and there is a delay time of 1 second between consecutive requests. Thus becuase the maximum amount of tweets that can be requested from a timeline at a time per user is 100, and the api stores the last 3200 tweets of each user, then for any username with over 3200 tweets, the program will take at least 32 seconds. This can be changed by modifying the variable MAX_TWEETS in constants.py such that the new max time of request execution will be floor(MAX_TWEETS / 100, 32). Similarly, although there is no cap on the amount of followers that one can pull, each followers request can at most pull 1000 followers. Right now, this is also the cap for the amount of followers the program will pull, but you can change it by modifying MAX_FOLLOWERS in constants.py.
- Twitter also caps certain request categories. You are only allowed to request followers from 15 users per 15 minutes and up to 500,000 tweets per month. Thus the --followers and --timeline flags are optional.
- All usernames cannot contain any non alphanumeric symbols. Thus instead of "@elonmusk" the input should be "elonmusk"

## Implementation/Design Choices
Currently the project is structured around the wrapper class TwitterUserScraper to allow for maximum abstractness. This class houses various implementations of the abstract class StandardRequester, where each implementation handles a different request. Thus, statistics that require different request can easily be added to the structure of the program by creating a child class of StandardRequester and adding an instance variable and calculate_values() line into TwitterUserScraper. Furthermore, many constants used within the requesters can be modified by changing the values in the constants.py file. For instance, you can add strings to certain dictionaries to request more parameters from the api with each corresponding requester. 

## Future Work
- I'm not entirely familar with industry standards for developing in python, thus there are most definetly infrastructural changes which could modernize the project.
- All variable-esque values in constants.py could be moved to an input config file argument for the project.
- With either Twitter enterprise or Twitter research, many logistical/time concerns with the runtime of the project could be massively improved.
- Multithreading could be used across different Requesters or perhaps different requests to speed up the project. 