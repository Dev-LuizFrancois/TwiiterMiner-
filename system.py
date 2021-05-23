
import tweepy
from user import User
from collections import Counter
    



class System:

    non_included_chars = [",", ".", "!", "?", "(", ")", "[", "]", "{", "}", ":"]
    name = ""
    RANKNUM = 5
    AT = "@"
    TAG = "#"

    def __init__(self, c_key, c_secret, a_key, a_secret):

        ### Twitter Handler ###
        self.auth = tweepy.OAuthHandler(c_key, c_secret)
        self.auth.set_access_token(a_key, a_secret)
        self.api = tweepy.API(self.auth)
        self.user = None
        self.filters = []



    ### AUX FUNCTIONS ####    

    def filter_switch(self, w_filter):
        if(len(self.filters) > 0):
            self.filters = []
        else:
            self.filters = w_filter

    ### SYSTEM MAIN FUNCITIONS ###

    def initialize(self, name):
        try:
            self.user = User(self.api, name)
            fetched_tweets = self.user.fetch()
            if(self.user.isFetched()):
                print("Foram cumputados ", fetched_tweets, " tweets.")
            return fetched_tweets
        except tweepy.TweepError:
            return -1

    def isProtected(self):
        return self.user.isProtected()
    def get_user_avatar(self):
        return self.user.get_user_avatar()

    def get_user_url(self):
        return self.user.get_user_url()
    
    def getName(self):
        return self.user.getName()

    def getNumFollowers(self):
        return self.user.getNumFollowers()
    
    def get_num_following(self):
        return self.user.get_num_following()
    
    def get_num_tweets(self):
        return self.user.get_num_tweets()

    def get_description(self):
        return self.user.get_description()

    def get_user_banner(self):
        return self.user.get_user_banner()
    
    def most_liked(self):
        return self.user.rank_likes(5)

    def most_retweeted(self):
        return self.user.rank_retweets(5)

    def common_word(self):
        
        if(len(self.filters)>0):
            all_w = [e for e in self.user.getAllWords() if e not in self.filters and len(e) > 3]
        else:
            all_w = self.user.getAllWords()
        
        return Counter(all_w).most_common(5)
    
    def get_all_words(self):
        return self.user.getAllWords()

    
    def common_hashtags(self):
        return Counter(self.user.getAllTags()).most_common(5)
    
    def common_interactions(self):
        res_lst = []
        for u in Counter(self.user.getAllInteractions()).most_common(5):
            res_lst.append((u[0], self.api.get_user(u[0]).profile_image_url_https, u[1]))
        return res_lst
        




        
        




    
        


