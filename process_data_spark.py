# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from settings import *
from many_stop_words import get_stop_words
from shapely.geometry import Polygon
from langdetect import detect

from nltk import wordpunct_tokenize
from nltk.probability import FreqDist, ConditionalFreqDist

import re, string, nltk, sys
import json, os, logging
from collections import defaultdict, Counter
from itertools import combinations

from pos_tag import postag_sents, segment_sents
from ner import *
import logger


def printu(lst, prnt=True):
    s = u'.'.join(lst).encode('utf-8')
    if prnt:
        print s
    else:
        return s   

    
def preprocess(txt):
    if not isinstance(txt,unicode):
        txt = unicode(txt, 'utf-8')
    
    txt = txt.replace(u"أ",u"ا")
    txt = txt.replace(u"إ",u"ا")
    txt = txt.replace(u"ى",u"ي")
    txt = re.sub(r'([^\s\w]|_)+', u' ', txt, flags=re.U)
    url = r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    txt = re.sub(url, u' ', txt, flags=re.U)
    
    return txt

          
def filter_words(words):
    new_words = FreqDist(words)
    stopwords = get_stop_words('ar')
    keys = new_words.keys()
    
    for word in keys:
        if word in stopwords:
            new_words.pop(word)
            
        if len(word) <= 2:
            new_words.pop(word)
            
    return new_words


def filter_token_tag(tok_tag, stopwords=get_stop_words('ar')):
    allowed_tags = ['NN', 'DTNN', 'NNS','NNP','NNPS', 'JJ', 'JJR', 'JJS']
    w, t = tok_tag

    if w in stopwords:
        return False
    if len(w) <= 2:
        return False
    try:
        if detect(w) != 'ar':
            return False
    except:
        return False
    if t not in allowed_tags:
        return False

    return True  


def filter_edges(edges, words):
    new_edges = []
    stopwords = get_stop_words('ar')
    edges_word = FreqDist()
    max_e = 10
    
    for e, w in edges:
        if e[0] in stopwords or e[1] in stopwords:
            continue
        
        if len(e[0]) <= 2 or len(e[1]) <= 2:
            continue
        
        if e[0] not in words and e[1] not in words:
            continue

        if edges_word[e[0]] >= max_e or edges_word[e[1]] >= max_e:
            continue
        
        new_edges.append((e,w))
        edges_word[e[0]] += 1
        edges_word[e[1]] += 1
            
    return new_edges


def summarize_text(txt):
    words = FreqDist()
    bigrams = FreqDist()
    txt = preprocess(txt)
    tokens = segment_sent(txt)
    
    for word in tokens:
        words[word] += 1
        
    for bg in nltk.bigrams(tokens):
        bigrams[bg] += 1        
        
    return words, bigrams, tokens


def reduce_text(t1, t2):
    words = FreqDist(t1[0])
    words.update(t2[0])

    try:
        bigrams = FreqDist(t1[1])
        bigrams.update(t2[1])
    except:
        logger.error('problem in reducing..')
        logger.error('t1: %s' % str(t1))
        logger.error('t2: %s' % str(t2))
    
    return words, bigrams


def summarize_tweet(tweet):
    if not tweet.get('text'):
        raise Exception('This is not a tweet.')
    
    words = FreqDist()
    tags = FreqDist() 
    places = FreqDist()
    bigrams = FreqDist()
    tokens = tweet['tokens']
    
    for word, tag in tokens:
        if tag in ['NN', 'DTNN', 'NNS','NNP','NNPS']:
            words[word] += 1
        
    for tag in tweet['hashtags']:
        tags[tag['text']] += 1
        
    if tweet['place']:
        places[ tweet['place']['name'] ] += 1
        
    for bg in nltk.bigrams([t[0] for t in tokens]):
        bigrams[bg] += 1

    return tags, words, places, bigrams                


def reduce_tweets(t1, t2):
    tags = FreqDist(t1[0])
    tags.update(t2[0])
    
    words = FreqDist(t1[1])
    words.update(t2[1])
    
    places = FreqDist(t1[2])
    places.update(t2[2])
    
    bigrams = FreqDist(t1[3])
    bigrams.update(t2[3])
    
    return tags, words, places, bigrams


def get_hashtags(tweet):
    hashtags = []
    hashtags_links = [tuple(sorted(l)) for l in combinations(tweet['hashtags'], 2)]
    
    for tag in tweet['hashtags']:
        hashtag = {'tweet_ids': [tweet['_id']],
                   'count': 1
                    }
        links = [lnk[1] for lnk in  hashtags_links if lnk[0]==tag]
        links = Counter(links)
        hashtag['links'] = links

        spread = []
        if tweet['loc']:
                spread = [tweet['loc']['coordinates']]
        #elif tweet['place']:
                #spread = Polygon(tweet['place']['bounding_box']['coordinates'][0]).centroid.coords[0]
        hashtag['spread'] = spread

        hashtags.append((tag, hashtag))

    return hashtags                    


def summarize_hashtags(d1, d2):
    result = {'count': d1['count'] + d2['count'],
              'tweet_ids': d1['tweet_ids'] + d2['tweet_ids'],
              'links': d1['links'] + d2['links'],
              'spread': d1['spread'] + d2['spread']
              }

    return result


def hashtag_json((tag, d)):
        d2 = dict(d.items() + [('hashtag',tag)])
        d2['links'] = [{'target': t[0], 'weight': t[1]} for t in d2['links'].items()]
        return d2


def get_words(d):
    words = []
    words_links = [tuple(sorted(l)) for l in combinations([t[0] for t in d['tokens']], 2)]
    
    for w, t in d['tokens']:
        word = {'count': 1}
        links = [lnk[1] for lnk in  words_links if lnk[0]==w]
        links = Counter(links)
        word['links'] = links
        words.append((w, word))

    return words                    



def summarize_words(d1, d2):
    result = {'count': d1['count'] + d2['count'],
              'links': d1['links'] + d2['links'],
              }

    return result


def word_json((w, d)):
        d2 = dict(d.items() + [('word',w)])
        d2['links'] = [{'target': t[0], 'weight': t[1]} for t in d2['links'].items()]
        return d2


def get_nes(d):
    nes = []
    tokens = [t[0] for t in d['tokens']]

    if not 'nes' in d:
        return nes
    
    for ne in d['nes']:
        nparts = len(ne)
        entity = {'count': 1}
        links = []
        
        for i in range(len(tokens)):
            if tokens[i:i+nparts] == ne:
                if i > 0: links.append(tokens[i-1])
                try : links.append(tokens[i+nparts])
                except: pass
                                   
        links = Counter(links)
        entity['links'] = links
        nes.append((' '.join(ne), entity))

    return nes                    



def summarize_nes(d1, d2):
    result = {'count': d1['count'] + d2['count'],
              'links': d1['links'] + d2['links'],
              }

    return result


def nes_json((ne, d)):
        d2 = dict(d.items() + [('entity',ne)])
        d2['links'] = [{'target': t[0], 'weight': t[1]} for t in d2['links'].items()]
        return d2



def read_json(d):
    def load(d):
        try:
            d = json.loads(d)
            return d
        except: pass

    return d.map(load).filter(lambda t: t!=None)


def process_partition(data):
    data = list(data)    
    try:
        txt = [preprocess(d['tweet']) for d in data]
    except:
        print data[0]
    #tokenized_txts = segment_sents(txt)
    tokenized_txts = [wordpunct_tokenize(t) for t in txt]
    tagged_txts = postag_sents(tokenized_txts)          # prepare POS tags list

    for tok_tags, d in zip(tagged_txts, data):
        tok_tags = filter(filter_token_tag, tok_tags)
        d['tokens'] = tok_tags

    ner_result = find_nes(data)         # prepare named entities list

    for nes, d in zip(ner_result, data):
        d['nes'] = nes

    return data


def main(data=None, fname=None):
    logger = logging.getLogger('.log')

    if data != None:
        data_rdd = sc.parallelize(data)
        
    elif fname:         #read data from file
        data_rdd = sc.textFile('%s://%s/%s' %(FILESYSTEM, APP_HOME, fname))
        data_rdd_json = read_json(data_rdd)
        
    else:           #read data from database
        data_rdd_json = sc.mongoRDD('mongodb://%s:%d/%s.tweets' %(MONGO_SERVER, MONGO_PORT, DB))
    data_rdd_json = data_rdd_json.mapPartitions(process_partition)

    # Hashtags and their network
    hashtags_rdd = data_rdd_json.flatMap(get_hashtags)           
    hashtags_rdd = hashtags_rdd.reduceByKey(summarize_hashtags)    
    hashtags_rdd = hashtags_rdd.map(hashtag_json)
    hashtags_rdd.saveToMongoDB('mongodb://%s:%d/%s.hashtags_data' %(MONGO_SERVER, MONGO_PORT, DB))

    # Words and their network
    words_rdd = data_rdd_json.flatMap(get_words)            
    words_rdd = words_rdd.reduceByKey(summarize_words)
    words_rdd = words_rdd.map(word_json)
    words_rdd.saveToMongoDB('mongodb://%s:%d/%s.words_data' %(MONGO_SERVER, MONGO_PORT, DB))

    '''places_rdd = data_rdd_json.flatMap(get_places)           
    places_rdd = places_rdd.reduceByKey(summarize_places)
    places_rdd.saveToMongoDB('mongodb://%s:%d/%s.places_data' %(MONGO_SERVER, MONGO_PORT, DB))'''

    # Named Entities and their network
    nes_rdd = data_rdd_json.flatMap(get_nes)           
    nes_rdd = nes_rdd.reduceByKey(summarize_nes)
    nes_rdd = nes_rdd.map(nes_json)
    nes_rdd.saveToMongoDB('mongodb://%s:%d/%s.nes' %(MONGO_SERVER, MONGO_PORT, DB))
    
            
if __name__ == '__main__':
    main()
    

