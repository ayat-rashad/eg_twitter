import pymongo
from pymongo import MongoClient
from scipy.cluster.vq import kmeans2
import json, numpy as np
from collections import Counter

from geopy.distance import vincenty
from geopy.geocoders import GoogleV3
from shapely.geometry import Polygon



class DataReader(object):
    def __init__(self, dbname='tweets_data', buildDB=False, source='test.json'):
        client = MongoClient('localhost', 27017)
        API_KEY = "AIzaSyCCa1e_jLdt8Qt1C79m7cRoEl2U7PkrSbI"
        self.geolocator = GoogleV3(api_key=API_KEY, timeout=6)
        
        if not buildDB:
            db = client[dbname]  
            self.db = db
        
        else:
            if dbname in client.database_names():
                client.drop_database(dbname)
                
            db = client[dbname]  
            self.db = db
            tweetsCol = db.tweets
            tweets = []
            
            with open(source,'r') as f:                    
                for line in f:
                    t = json.loads(line)
                    coordinates = None
                    place = None

                    if t['coordinates']:
                        coordinates = t['coordinates']['coordinates']

                    if t['place']:
                        if t['place']['country_code'] != 'EG':
                            continue
                        place = t['place']['name']
                        if not coordinates:
                            coordinates = Polygon(t['place']['bounding_box']['coordinates'][0]).centroid.coords[0]

                    t2 = {'_id': t['id'], 'loc':{ 'type':'Point', 'coordinates': coordinates},
                        'place': place, 'hashtags': [ht['text'] for ht in t['hashtags']],
                        'tweet': t['text'], 'retweets': t['retweets'], 'time': t['time']}
                    tweets.append(t2)
                    
            try:
                result = tweetsCol.insert_many(tweets)
            except Exception as e:
                print e
                print 'ERROR inserting tweets.'
                return
                
            tweetsCol.create_index([('loc', pymongo.GEOSPHERE)])
                
    
    def cluster(self, cells):
        X = np.array([c['loc']['coordinates'] for c in cells])
        k = len(X)/100
        cluster_centroids, closest_centroids = kmeans2(X, k, minit='points')
        count = Counter(closest_centroids)
        cluster_cells = [[cells[i]['_id'] for i in range(len(closest_centroids)) if closest_centroids[i]==j]
                        for j in range(len(cluster_centroids))]
        clusters  = [{'loc':{ 'type':'Point', 'coordinates':c.tolist() }, 'count':count[i],
                    'cells': cluster_cells[i]} for i,c in enumerate(cluster_centroids)]

        return clusters

        
    def get_by_area(self, s, n, e, w, includeTweet, NTags):
        cursor = self.db.hashtags.find({'loc': {'$geoWithin': 
                                                {'$polygon': [  [ e, s ], [ e, n ], [ w, n ], [ w, s ],[ e, s ] ]}}
                                       },
                                       {'tweet':includeTweet}
                                     ).aggregate([{'$unwind':'$hashtags'},
                                                  {'$group':{'_id':'$hashtags', 'mentions': { '$sum': 1 }}
                                                    }])
        cursor.sort([('mentions', pymongo.DESCENDING)]).limit(NTags)
        
        return list(cursor)

        
    def get_by_hashtag(self, sortBy, includeTweet, NTags):
        cursor = self.db.hashtags.find({}, {'_id':0})
        cursor.sort([(sortBy, pymongo.DESCENDING)]).limit(NTags)
        
        return list(cursor)


    def get_hashtag(self, htag, includeTweet, s, n, e, w):
        result = self.db.hashtags.find({'hashtag': htag}, {'_id':0, 'places':1})
        result = list(result)

        if includeTweet:
            tweets = self.db.tweets.find({"hashtags": {"$in":[htag]},
                                          "loc": {'$geoWithin':
                                                 {'$polygon': [  [ e, s ], [ e, n ], [ w, n ], [ w, s ],[ e, s ] ]}}
                                          }, {"_id":0, "loc":1, "tweet":1})
            tweets = list(tweets)
            result[0]['tweets'] = tweets
        
        return result
                                       
                                       
                            
