# -*- coding: utf-8 -*-
from nltk import wordpunct_tokenize
from nltk.probability import FreqDist, ConditionalFreqDist

import re, string, nltk, sys
import json, os, logging
from collections import defaultdict

from pos_tag import postag_sents, segment_sents
from langdetect import detect


#Buckwalter transliteration table
buck2uni = {"'": u"\u0621", # hamza-on-the-line
            "|": u"\u0622", # madda
            ">": u"\u0623", # hamza-on-'alif
            "&": u"\u0624", # hamza-on-waaw
            "<": u"\u0625", # hamza-under-'alif
            "}": u"\u0626", # hamza-on-yaa'
            "A": u"\u0627", # bare 'alif
            "b": u"\u0628", # baa'
            "p": u"\u0629", # taa' marbuuTa
            "t": u"\u062A", # taa'
            "v": u"\u062B", # thaa'
            "j": u"\u062C", # jiim
            "H": u"\u062D", # Haa'
            "x": u"\u062E", # khaa'
            "d": u"\u062F", # daal
            "*": u"\u0630", # dhaal
            "r": u"\u0631", # raa'
            "z": u"\u0632", # zaay
            "s": u"\u0633", # siin
            "$": u"\u0634", # shiin
            "S": u"\u0635", # Saad
            "D": u"\u0636", # Daad
            "T": u"\u0637", # Taa'
            "Z": u"\u0638", # Zaa' (DHaa')
            "E": u"\u0639", # cayn
            "g": u"\u063A", # ghayn
            "_": u"\u0640", # taTwiil
            "f": u"\u0641", # faa'
            "q": u"\u0642", # qaaf
            "k": u"\u0643", # kaaf
            "l": u"\u0644", # laam
            "m": u"\u0645", # miim
            "n": u"\u0646", # nuun
            "h": u"\u0647", # haa'
            "w": u"\u0648", # waaw
            "Y": u"\u0649", # 'alif maqSuura
            "y": u"\u064A", # yaa'
            "F": u"\u064B", # fatHatayn
            "N": u"\u064C", # Dammatayn
            "K": u"\u064D", # kasratayn
            "a": u"\u064E", # fatHa
            "u": u"\u064F", # Damma
            "i": u"\u0650", # kasra
            "~": u"\u0651", # shaddah
            "o": u"\u0652", # sukuun
            "`": u"\u0670", # dagger 'alif
            "{": u"\u0671", # waSla
}


def transString(string, reverse=0):
    if not reverse:     
        for k,v in buck2uni.iteritems():
            string = string.replace(v,k)

    else:     
        for k,v in buck2uni.iteritems():
            string = string.replace(k,v)

    return string


def read_sents(fname='nes.txt'):
    LINE_DELIM = '##'
    
    def read(f):
        sent = []
        for token in f:
            token = token.strip()
            if not token.startswith(LINE_DELIM):
                sent.append(tuple(token.split(' ')))
            else:
                yield sent
                sent = []

    with open(fname) as f:
        sents = [sent for sent in read(f)]

    return sents


def write_sents(data, fname='trans.txt'):
    LINE_DELIM = '##'
    
    with open(fname, 'w') as f:
        for d in data:
            txt = '\n'.join([t[0] for t in d['trans_tokens']])
            txt += '\n%s\n' % LINE_DELIM
            try:
                f.write(txt)
            except UnicodeEncodeError as e:
                f.write(txt.encode('utf-8'))

                
def find_nes(data):         #find named entities
    for d in data:
        d['trans_tokens'] = [(transString(t[0]), t[1]) for t in d['tokens']]    #transliterate tokens

    infile = "trans.txt"
    outfile = "nes.txt"
    write_sents(data)
    result = subprocess.call(["yamcha", "-m NER.model", infile, "-o %s" %outfile])

    if result != 0:
        print("NER process error.")
        return False

    ner_result = read_sents(outfile)

    for nes, d in zip(ner_result, data):
        ne_list = [ne for ne in nes if ne[1]!='O']
        d['nes'] = ne_list


def find_colloc(data):          #find most common collocations
    def check(wb, tb):
        if len(wb[0]) <= 1 or len(wb[1]) <= 2:
            return False
        try:
            if detect(wb[0]) != 'ar' or detect(wb[1]) != 'ar':
                return False
        except:
            return False
        
        if tb in [('NN','NN'),('NN','DTNN'), ('NNP','NNP')]:
            return True
        return False
        
    bigrams = FreqDist()

    for d in data:
        tokens = d['tokens']
        words_bigrams = nltk.bigrams([t[0] for t in tokens])
        tags_bigrams = nltk.bigrams([t[1] for t in tokens])
            
        for wb, tb in zip(words_bigrams, tags_bigrams):
            if check(wb, tb):
                bigrams[wb] += 1

    return bigrams


def read_json(data):
    def load(d):
        try:
            d = json.loads(d)
            return d
        except: pass
    data = map(load, data)
    data = filter(lambda t: t!=None, data)

    return data


def process_partition(data):
    pass


if __name__ == '__main__':
    '''data = []

    with open('test.json') as f:
        data = read_json(f.readlines())

    data = process_partition(data)
    transliterate(data)'''
    '''bigrams = find_nes(data)
    top = bigrams.most_common(50)

    for ne in top:
        printu(ne[0])'''
        

    
