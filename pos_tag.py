# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nltk.tag import StanfordPOSTagger
from stanford_segmenter import StanfordSegmenter
from settings import *
import os


def postag_sents(sents):
    if not os.environ.get('STANFORD_MODELS'):
        base = APP_HOME + '/stanford-postagger'
        os.environ["STANFORD_MODELS"] = base + '/models'
        
    st = StanfordPOSTagger('arabic.tagger', base+'/combined.jar')
    tagged_sents = st.tag_sents(sents)
    tagged_sents = [[tuple(t[1].split('/'))  for t in sent] for sent in tagged_sents]
    
    return tagged_sents


def segment_sents(sents):
    if not os.environ.get('STANFORD_SEGMENTER'):
        os.environ['STANFORD_SEGMENTER'] = 'APP_HOME' + '/stanford_segmenter'
        
    segmenter = StanfordSegmenter()
    tokens = segmenter.segment_sents(sents)

    return tokens


if __name__=='__main__':
    pass

