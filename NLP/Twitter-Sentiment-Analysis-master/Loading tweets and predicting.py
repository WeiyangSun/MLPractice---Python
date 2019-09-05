from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import json
from nltk.corpus import stopwords
from nltk import word_tokenize
import pickle

stop_words= set(stopwords.words("english"))

ckey="VeSEVRVC6Vt25pUSrLSUzt2nG"
csecret="CskqeBbwBf5pHc6GmPRFCEDRBlYLaWpBv9BbcsgxiGMdUincjg"
atoken="909074170683764736-KlfVMKqpGHXtHHU1uVZFMKM7Jx7Pgwh"
asecret="dpNKsYxzl13kAguwyksdeqNbGNRPJW4xIIp6hCy6dDDBn"

pickle_out=open("/Users/pushkarsingh/Desktop/twitter/pos-yy_adj.pickle","rb")
pos_adj=pickle.load(pickle_out)

pickle_out=open("/Users/pushkarsingh/Desktop/twitter/neg-yy_adj.pickle","rb")
neg_adj=pickle.load(pickle_out)

def check(example):
    pos_count=0
    neg_count=0
    ex_words=word_tokenize(example)

    for ex_word in ex_words:
        if ex_word.lower() not in stop_words:
            for key, value in pos_adj.items():
                if key==ex_word.lower():
                    pos_count+=value
            for key, value in neg_adj.items():
                if key==ex_word.lower() :
                    neg_count+=value

    if pos_count>neg_count:
        conf=pos_count-neg_count
        checker="pos"
        
            
    elif pos_count<neg_count:
        conf=neg_count-pos_count
        checker="neg"
       
    elif pos_count==neg_count:
        checker="None"
        conf=0
        
    return checker, conf
try:
    os.remove("/Users/pushkarsingh/Desktop/twitter/test-yy_twitter.txt")
    
except:
    output = open("/Users/pushkarsingh/Desktop/twitter/test-yy_twitter.txt","a")
    
class listener(StreamListener):

    def on_data(self, data):
        tweets = json.loads(data)
        tweet = tweets["text"]
        created_date=tweets['created_at']
        label,con=check(tweet)
        output = open("/Users/pushkarsingh/Desktop/twitter/test-yy_twitter.txt","a")
        output.write(label)
        output.write('\n')
        #print(con)
        return True

    def on_error(self, status):
        if status=="420":
            print(status)
            print("Multiple Connections, Try again after sometime")
        else:
            print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Terrorist"])
output.close()
