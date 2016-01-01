from importlib import import_module
import json, sys
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.oauth import OAuth
from twitter.util import printNicely

def main():
    try:
        filename = sys.argv[1]
    except:
        filename = 'tweets.json'
    out = open(filename, 'a')

    try:
        con = import_module(sys.argv[2])
    except:
        con = import_module('config')
    auth = OAuth(con.TOKEN, con.TOKEN_SECRET, con.CONSUMER_KEY, con.CONSUMER_SECRET)
    
    '''stream_args = dict(
        timeout=args.timeout,
        block=not args.no_block,
        heartbeat_timeout=args.heartbeat_timeout)'''
        
    stream_args = {}
    query_args = {"locations": con.COORDS}    
    stream = TwitterStream(auth=auth)
    tweet_iter = stream.statuses.filter(**query_args)
    
    for tweet in tweet_iter:
        if tweet is None:
            printNicely("-- None --")
        elif tweet is Timeout:
            printNicely("-- Timeout --")
        elif tweet is HeartbeatTimeout:
            printNicely("-- Heartbeat Timeout --")
        elif tweet is Hangup:
            printNicely("-- Hangup --")
        elif tweet.get('text'):
            tweetJson = {"id":tweet['id_str'], "time":tweet['created_at'], "place":tweet['place'],"coordinates":tweet['coordinates'], "retweets":tweet['retweet_count'], "text": tweet['text'], "hashtags": tweet['entities']['hashtags']}
            out.write(json.dumps(tweetJson)+"\n")
        else:
            printNicely("-- Some data: " + str(tweet))
            
            
if __name__ == '__main__':
    main()
