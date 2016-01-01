# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyspark import SparkContext, SparkConf
from many_stop_words import get_stop_words
from nltk.probability import FreqDist, ConditionalFreqDist
import re, string, nltk,sys
from nltk import wordpunct_tokenize
from pos_tag import postag_sents, segment_sents
import json
import logger
import logging


logger = logging.getLogger('.log')
conf = SparkConf().setAppName('eg_twitter').setMaster('local')
sc = SparkContext(conf=conf)

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
    
    return txt

            
def summarize(data):
    words = FreqDist()
    tags = FreqDist() 
    places = FreqDist()
    bigrams = FreqDist()
    stopwords = get_stop_words('ar')   
    
    for tweet in data:
        txt = preprocess(tweet['text'])
        tokens = wordpunct_tokenize(txt)
        for word in tokens:
            words[word] += 1
            
        for tag in tweet['hashtags']:
            tags[tag['text']] += 1
            
        if tweet['place']:
            places[ tweet['place']['name'] ] += 1
            
        for bg in nltk.bigrams(tokens):
            bigrams[bg] += 1
                        
    for word in words:
        if word in stopwords:
            words.pop(word)
                                   
    print 'Top 50 hashtags:', printu([t[0] for t in tags.most_common(50)])
    print 'Top 50 words:', printu([w[0] for w in words.most_common(50)])
    print 'Top 10 places:', printu([p[0] for p in places.most_common(10)])
    
    return tags, words, places

          
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
        return
    
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


def read_json(d):
    def load(d):
        try:
            d = json.loads(d)
            return d
        except: pass

    return d.map(load).filter(lambda t: t!=None)


def process_partition(data):
    data = [d for d in data]
    txt = [preprocess(d['text']) for d in data]
    tokenized_txts = segment_sents(txt)
    tagged_txts = postag_sents(tokenized_txts)

    for d in data[-1::-1]:
        d['tokens'] = tagged_txts.pop()

    return data


def main(data=None, fname='test.json'):
    if data != None:
        data_rdd = sc.parallelize(data)
    else:
        data_rdd = sc.textFile(fname)
        
    data_rdd_json = read_json(data_rdd)
    data_rdd_json = data_rdd_json.mapPartitions(process_partition)
    tags, words, places, bigrams = data_rdd_json.map(summarize_tweet).reduce(reduce_tweets)
    words = filter_words(words) 
    
    logger.info( 'Top 50 hashtags:')
    print( 'Top 50 hashtags:')
    logger.info(printu([t[0] for t in tags.most_common(50)], False))
    printu([t[0] for t in tags.most_common(50)])
    logger.info( 'Top 50 words:')
    print( 'Top 50 words:')
    logger.info(printu([w[0] for w in words.most_common(50)], False))
    printu([w[0] for w in words.most_common(50)])
    logger.info( 'Top 10 places:')
    print( 'Top 10 places:')
    logger.info(printu([p[0] for p in places.most_common(10)], False))
    printu([p[0] for p in places.most_common(10)])
    logger.info( 'Top 10 bigrams:')
    print( 'Top 10 bigrams:')
    logger.info(printu([' '.join(bg[0]) for bg in bigrams.most_common(10)], False))
    printu([' '.join(bg[0]) for bg in bigrams.most_common(10)])
    
            
if __name__ == '__main__':
    main()
    
    
