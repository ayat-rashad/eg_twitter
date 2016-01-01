# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nltk.tag import StanfordPOSTagger
from stanford_segmenter import StanfordSegmenter
import os


def postag_sents(sents):
    if not os.environ.get('STANFORD_MODELS'):
        base = os.getcwd()+'/stanford-postagger'
        os.environ["STANFORD_MODELS"] = base+'/models'
        os.environ['CLASSPATH'] = base
        
    st = StanfordPOSTagger('arabic.tagger', base+'/combined.jar')
    tagged_sents = st.tag_sents(sents)
    tagged_sents = [[tuple(t[1].split('/'))  for t in sent] for sent in tagged_sents]
    
    return tagged_sents


def segment_sents(sents):
    if not os.environ.get('STANFORD_SEGMENTER'):
        os.environ['STANFORD_SEGMENTER'] = 'stanford_segmenter'
        
    segmenter = StanfordSegmenter()
    tokens = segmenter.segment_sents(sents)

    return tokens


if __name__=='__main__':
    sents = [u'دي الجملة الأولى', u'ودي الجملة التانية']
    tokens = segment_sents(sents)
    tagged_tokens = postag_sents(tokens)
    for sent in tagged_tokens:
        print u','.join([u'#'.join(t) for t in sent])
        #for t in sent:
            #print('#'.join(t))



