#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from __future__ import unicode_literals, print_function
 
import tempfile
import os, re
import json, string
from subprocess import PIPE
 
from nltk import compat
from nltk.internals import find_jar, config_java, java, _java_options
from nltk.tokenize.api import TokenizerI
 
class StanfordSegmenter(TokenizerI): 
    _JAR = 'stanford-segmenter.jar'
 
    def __init__(self, path_to_jar=None,
            path_to_model='data/arabic-segmenter-atb+bn+arztrain.ser.gz',
            encoding='UTF-8', options=None,
            verbose=False, java_options='-mx300m'):

        if not os.environ.get('STANFORD_SEGMENTER'):
            os.environ['STANFORD_SEGMENTER'] = 'stanford_segmenter'
            
        self._stanford_jar = find_jar(
                self._JAR, path_to_jar,
                env_vars=('STANFORD_SEGMENTER',),
                searchpath=(),
                verbose=verbose
            )
        self._model = os.environ['STANFORD_SEGMENTER'] + '/%s' %path_to_model
        self._encoding = encoding
        self.java_options = java_options
        options = {} if options is None else options
        self._options_cmd = ','.join('{0}={1}'.format(key, json.dumps(val)) for key, val in options.items())
 

    def segment_file(self, input_file_path, out_file_path='out.txt'):
        cmd = [
            'edu.stanford.nlp.international.arabic.process.ArabicSegmenter',
            '-textFile', input_file_path,
            '-loadClassifier', self._model,
            
        ]
 
        stdout = self._execute(cmd)
        with open(out_file_path, 'w') as  f:
            for line in stdout:
                f.write(line.encode('utf-8'))
        return stdout
    
 
    def segment(self, tokens):
        return self.segment_sents([tokens])
 

    def segment_sents(self, sentences):
        encoding = self._encoding
        _input_fh, self._input_file_path = tempfile.mkstemp(text=True)      # Create a temporary input file
        _input_fh = os.fdopen(_input_fh, 'wb')      # Write the actural sentences to the temporary input file
        _input = u'\n'.join(sentences)
        
        if isinstance(_input, compat.text_type) and encoding:
            _input = _input.encode(encoding)
            
        _input_fh.write(_input)
        _input_fh.close()
 
        cmd = [
            'edu.stanford.nlp.international.arabic.process.ArabicSegmenter',
            '-textFile', self._input_file_path,
            '-loadClassifier', self._model,
        ]
 
        stdout = self._execute(cmd)
        os.unlink(self._input_file_path)        # Delete the temporary file
 
        return [line.split(u' ') for line in stdout.split(u'\n') if not re.match(r'^\s*$', line)]
 

    def _execute(self, cmd, verbose=False):
        encoding = self._encoding
        #cmd.extend(['-inputEncoding', encoding])
        _options_cmd = self._options_cmd
        if _options_cmd:
            cmd.extend(['-options', self._options_cmd])
 
        default_options = ' '.join(_java_options)
 
        config_java(options=self.java_options, verbose=verbose)     # Configure java.
        stdout, _stderr = java(cmd,classpath=self._stanford_jar, stdout=PIPE, stderr=PIPE)
        stdout = stdout.decode(encoding)
        config_java(options=default_options, verbose=verbose)       # Return java configurations to their default values.
 
        return stdout
 


if __name__=='__main__':
    base = 'stanford_segmenter'
    os.environ['STANFORD_SEGMENTER'] = base
    os.environ['CLASSPATH'] = base + 'stanford-segmenter-3.6.0.jar:' + base +'slf4j-api.jar'
    segmenter = StanfordSegmenter()
    #stdout = segmenter.segment_file('sample.txt')
    #for line in stdout: print(line)
    with open('sample.txt') as f:
        tokens = segmenter.segment_sents([unicode(line,'utf-8') for line in f])
        for t in tokens:    print(t)
    
