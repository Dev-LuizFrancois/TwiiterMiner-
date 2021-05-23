# `Twitter Miner`

Upon receiving a specific Twitters user '@', this programm fetches the users tweets timeline and saves it to a .JSON formatted file, that is than handkled by Tweepy to a Cursos object. Twitter limits the amount of tweets that can be downloaded per 15 minutes. Thus, when an exception is raised (i.e., the maximum allowed number of tweets has been reached) the script will wait for the time needed and then resume the analyzes. 

The user interface allows for 5 different data analyzes of the tweets timeline, that are detailed on the section `4. Data Analysis` below. The frontend was developed using Javascript, HTML5 and Bootstrap Framework, and integrated with the script with Pythons Flask Library. To achieve a client-side data session, [KvSession](https://pythonhosted.org/Flask-KVSession/) was used in addition to the Flask session.

The main script uses Tweepy library as well as Twitters official API. The links for the Twitters official API and Tweepy Library are in the Links section below.

This project was developed by me during my first year as a Computer Engineer Student (2019), with the intention of learning more about different Python Libraries, as well as working with a robust API and frontend development.

---

## 1. Installation


Ensure you have python 3.6+ installed.

```bash
pip install -r requirements.txt
```

You can run a local server for test purposes with Redis-Server:

```bash
redis-server /usr/local/.../redis.conf
cd /TwiiterMiner
python webapp.py
```
---

## 2. Twitter Authentication


In addition, you'll need a personal Twitter Developers account. By registering yourself, you will generate  a consumer key, consumer secret, access token, and access secret; these are required to authenticate the script in order to access the Twitter API:

- Save the python file or download/clone the repository to your local machine. Make sure you have the dependencies.

- Open the webapp.py file and then find  and add your consumer key, consumer secret, access token, and access secret on the following fields:

        CONSUMER_KEY = 'CONSUMER KEY HERE'
        CONSUMER_SECRET = 'CONSUMER SECRET HERE'
        ACCESS_KEY = 'ACCESS TOKEN HERE'
        ACCESS_SECRET = 'ACCESS SECRET HERE'


---

## 3. Data Analysis

Upon inserting the desired `@` you want the analyses of, the cript fetches the main information of the account: avatar image, description, number of followers, retweeets and tweets.

These are the commands avaiable:

* `Most Used #`: Shows the top 5 most used hashtags by the specif user, aswell as the number of times they were used.



* `Most Interected @`: shows the profile image and name of the top 5 other users whose `@user` interacted with. By interaction, it is considered responses, retweets and mentions rate. Note that the user can interect with himself, and it will be showed in the ranking if so.

* `Most Common Word`: the script reads every single word that has been typed and shows the top 5 most used words. On the user interface, it is presented the option to filter the words considered by size or by words you don't want to be read. 

* `Most Liked Tweets`: embbeds the 5 most liked tweets made by the specific user.

* `Most Retweeted Tweets`: embbeds the tweets of the specific user that got the most retweets. Note that the tweets wich the specif user retweeted are counted as being part of his timeline, thus the author of the resulting tweets is not always the user.


---
## 4. Links


- [Tweepy Documentation](https://tweepy.readthedocs.io/en/latest/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
