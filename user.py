import tweepy
import heapq
import time

class Tweet:
    def __init__(self, text, url, num_likes, num_retw):
        self.text = text
        self.url = url
        self.num_likes = num_likes
        self.num_retw = num_retw
            
    def getText(self):
        return self.text
    
    def getUrl(self):
        return self.url
    
    def getNumLikes(self):
        return self.num_likes

    def getNum_retw(self):
        return self.num_retw

class User:
    def __init__(self, api, name):
        self.api = api
        self.user = self.api.get_user(name)
        self.timeline = []
        self.all_words = []
        self.all_tags = []
        self.all_interactions = []
        self.follows = self.user.friends()
        self.fetched = False
        self.tw_likes = []
        self.tw_retweets = []

    def getAllTags(self):
        res = []
        for t in self.all_tags:
            res.append(t.get("text"))

        return res

    def isProtected(self):
        return self.user.protected

    def get_user_url(self):
        return self.user.url
    
    def get_user_banner(self):
        return "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"

    def get_user_avatar(self):
        return self.user.profile_image_url_https
    
    def getName(self):
        return self.user.screen_name

    def getNumFollowers(self):
        return self.user.followers_count
    
    def get_num_following(self):
        return self.user.friends_count
    
    def get_num_tweets(self):
        return self.user.statuses_count

    def get_description(self):
        if(self.user.description == None):
            return "This user has no description!"
        else:
            return self.user.description

    ''' The actual rankiong of the collections is made by system, through a Counter'''
    def rank_likes(self, n): return heapq.nlargest(n, self.tw_likes)

    def rank_retweets(self, n): return heapq.nlargest(n, self.tw_retweets)

    def getAllWords(self): return self.all_words
    
    def getAllInteractions(self): return self.all_interactions

    ''' Inserts the tweets words into the words collection '''
    def feedAllWords(self, new_words):
        for w in new_words:
            if (w[0] not in ["@", "#"]):
                self.all_words.append(w)

    ''' Handles the cursor Item
    updating the collections with the matching data '''
    def process_data(self, t):
        #Non original status: retweet
        if(t.retweeted):
            ot = t.retweeted_status
            self.all_interactions.append((ot.user.screen_name))

        #original status:
        else:
            tweet = Tweet(t.full_text.split(),t.source_url, t.favorite_count, t.retweet_count)
            
            #extract words
            self.feedAllWords(tweet.getText())

            #extract hashtags
            self.all_tags.extend(t.entities.get("hashtags"))
            
            #extract mentions to other users, being responses or normal mentions
            if(t.in_reply_to_screen_name != None):
                self.all_interactions.append(t.in_reply_to_screen_name)
            else:
                mentions = t.entities.get("user_mentions")
                for m in mentions:
                    self.all_interactions.append(m.get("screen_name"))

            #Update heaps
            heapq.heappush(self.tw_likes, (t.favorite_count, t.id_str))
            heapq.heappush(self.tw_retweets, (t.retweet_count, t.id_str))

            self.timeline.append(tweet)

    ''' Fetches the tweets from twitter. If the amount of data is superior to limit
        waits for the 'penalty time' to continue '''
    def fetch(self):
        i = 0

        api_timeline = tweepy.Cursor(self.api.user_timeline,id=self.getName(), tweet_mode="extended").items()

        while True:
            try:
                self.process_data(api_timeline.next())
                i += 1
                print("Fetching ", i, " tweets...")

            except tweepy.TweepError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                self.fetched = True
                return len(self.timeline)

    def isFetched(self): return self.fetched


