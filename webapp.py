from flask import Flask, render_template, send_from_directory, request, session
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from system import System
from collections import Counter

''' Redis local server setup '''
store = RedisStore(redis.StrictRedis())

''' Flask and KV Session setup '''
app = Flask(__name__, static_folder="static")
app.secret_key = "customsecretkey"
KVSessionExtension(store, app)


''' Twitter DEvelopers Account Authentication '''

        CONSUMER_KEY = 'CONSUMER KEY HERE'
        CONSUMER_SECRET = 'CONSUMER SECRET HERE'
        ACCESS_KEY = 'ACCESS TOKEN HERE'
        ACCESS_SECRET = 'ACCESS SECRET HERE'


''' Routes '''
### Home Page ###
@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("tweetMiner.html", error = False)

### Main Script initialization: after request ###
@app.route("/request", methods=["GET", "POST"])
def tweet_miner_send():
    
    if request.method == 'POST':

        at = request.form['at_input']

        ### Empty form
        if(len(at) == 0):
            return render_template("tweetMiner.html", error = True, error_msg=" Please, input the @ of the user you want to analyze!")

        ### Tweepy Object ###
        sys = System(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
        fetched = sys.initialize(at)

        ### Connection error to the API Handler ###
        if(fetched == -1):
            return render_template("tweetMiner.html", error = True, error_msg=" We cannot process any tweets right now. Please try again later.")

        ### Session spaces distribution ###
        if(not sys.isProtected()):
            session["num_tweets"] = fetched
            session["status"] = 0
            session["user_name"] = sys.getName()
            session["num_followers"] = sys.getNumFollowers()
            session["num_following"] = sys.get_num_following()
            session["description"] = sys.get_description()
            session["user_avatar"] = sys.get_user_avatar()
            session["most_hash"] = sys.common_hashtags()
            session["most_inter"] = sys.common_interactions()
            session["all_words"] = sys.get_all_words()
            session["most_liked"] = sys.most_liked()
            session["most_ret"] = sys.most_retweeted()
        
        ### Private User ###
        else:
            return render_template("tweetMiner.html", error = True, error_msg=" The user you are trying to analyze is a private user! Try a different one. ")

        
        return render_template("minerRes.html", session=session)

    else:
        return render_template("tweetMiner.html", session=session)


@app.route("/loading", methods=["GET", "POST"])
def loading_screen():
    return render_template("loading.html")

@app.route("/tweetMiner/res", methods=["GET", "POST"])
def tweet_miner_func():
    if request.method == "POST":

        ''' Triggers for the main div in HTML '''
        if (request.form.get("profile")):
            session["status"] = 0
        if (request.form.get("most_hash")):
            session["status"] = 1
        if (request.form.get("most_at")):
            session["status"] = 3
        if (request.form.get("most_word")):
            session["status"] = 2
            all_w = session["all_words"]

           
            ''' Filter checkbox: get the words wich are not supposed to be included in the count '''
            if request.form.get("words_len"):
                wanted_len = int(request.form.get("words_len"))
            else:
                wanted_len = 3
            ''' checkbox that triggers the filter option '''
            if request.form.get("filter_on"):
                filters = request.form["filters"].split()
                if(len(filters) > 0):
                    filtered_words = [e for e in all_w if e not in filters and len(e) > wanted_len]
                    session["most_word"] = Counter(filtered_words).most_common(5)
            else:
                filtered_words = [e for e in all_w if len(e) > wanted_len]
                session["most_word"] = Counter(filtered_words).most_common(5)

        if (request.form.get("back_most_word")):
            session["status"] = 2
            all_w = session["all_words"]
            wanted_len = 3
            filtered_words = [e for e in all_w if len(e) > wanted_len]
            session["most_word"] = Counter(filtered_words).most_common(5)
        
        if(request.form.get("most_lkd")):
            session["status"] = 4
        
        if(request.form.get("most_ret")):
            session["status"] = 5

        return render_template("minerRes.html", session=session)



### Image handler ###    
@app.route('/<path:filename>')  
def send_file(filename):  
      return send_from_directory('/static/img', filename)


if __name__:
    app.run(debug=True)
