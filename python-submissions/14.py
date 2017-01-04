#!/usr/bin/python
# -*- coding=utf-8 -*-
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division
from __future__ import print_function

import codecs
import json
import sys

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize



# It is okay to include tokenization and symbols in the average word size count.
# Use the Thorn character (þ) to separate the fields
# Be sure to include coding=utf-8 to the first or second line

# All the output can be printed to the screen

# Note, when printing to a non-unicode terminal or using linux to write to a file
# http://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file

# You may need to download a corpus in nltk using the nltk.download() command.
# If you are having trouble completing feel free to post a message on the forum.

# Usage: PYTHONIOENCODING=UTF-8 python process-data.py > output.txt


with codecs.open("twitter.txt", encoding='utf-8') as f:
    c1 = open("Verra_Unit2.2_SC.csv", "w")
    lines = f.read()
    token_s = sent_tokenize(lines)
    line_num = 0
    for sent in token_s:
        token_w = word_tokenize(sent)
        avg_word = float(sum(map(len, token_w))) / len(token_w)
        print(line_num,'þ','"',sent.encode('utf-8'),'"','þ',avg_word, sep='', file = c1)
        line_num += 1
    c1.close()

    c2 = open("Verra_Unit2.2_SC.xml", "w")
    print('<document>','\n','  <sentences>','\n', file = c2)
    line_num = 0
    for sent in token_s:
        token_w = word_tokenize(sent)
        avg_word = float(sum(map(len, token_w))) / len(token_w)
        print('  <sentence id="',line_num,'">','\n','    <text>',sent.encode('utf-8'),'</text>','\n','    <avg>',
              avg_word,'</avg>','\n','    </sentence>','\n', sep = '', file = c2)
        line_num += 1
              
    print('\n','  </sentences>', '\n', '</document>', file = c2)
    c2.close()
        
    c3 = open("Verra_Unit2.2_SC.json", "w")
    print('{','\n','   "documents": {','\n','        "sentences": [','\n',file = c3)
    line_num = 0
    first = False
    for sent in token_s:
        token_w = word_tokenize(sent)
        avg_word = float(sum(map(len, token_w))) / len(token_w)
        if first is False:
            print('            {','\n','                "avg": ',avg_word,',','\n','                "id": ',line_num,',','\n',
              '                "text": "',(sent.encode('utf-8').replace('\n','')),'"','\n','            }', sep = '', file = c3)
            first = True
        else:    
            print(',','\n','            {','\n','                "avg": ',avg_word,',','\n','                "id": ',line_num,',','\n',
                  '                "text": "',(sent.encode('utf-8').replace('\n','')),'"','\n','            }', sep = '', file = c3)
        line_num += 1
              
    print('        ]','\n','    }','\n','}','\n',file = c3)
    c3.close()        
    pass
