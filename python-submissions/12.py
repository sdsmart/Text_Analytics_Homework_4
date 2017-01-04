#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division

import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

import csv

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
##CSV file
    raw = f.read().replace('\n',' ')
    
    outputfile = open("csvoutput.csv", "wb")
    
    sent_tokens = sent_tokenize(raw)
    
    counter = 0
                
    for s in sent_tokens:
            
        words = word_tokenize(s)
        avg = str(sum(len(word)for word in words)/len(words))
        count = str(counter)
        counter += 1
                
        newline = count + u"\u00FE"  + s + u'\u00FE'  + avg
        writer = csv.writer(outputfile, delimiter='\xfe', quotechar='"')
        row = []
        row.append(newline.strip().encode("utf-8"))
        writer.writerows([row])


##XML file
    file = open("xmloutput.xml","wb")

    counter = 0
    file.write("<document>\n")
    file.write("\t<sentences>\n")

    for s in sent_tokens:
        words = word_tokenize(s)
        avg = str(sum(len(word)for word in words)/len(words))
        count = str(counter)
        file.write('\t\t<sentence id="' + count + '">\n')
        file.write('\t\t\t<text>'+s.encode("utf-8")+'</text>\n')
        file.write('\t\t\t<avg>'+avg+'</avg>\n')
        file.write('\t\t</sentence>\n')
        counter += 1

    file.write("\t</sentences>\n")
    file.write("</document>\n")

    file = open("jsonoutput.json","wb")

## JSON file
    counter = 0
    file.write('{\n\t"documents":{\n')
    file.write('\t\t"sentences":[\n\t\t\t{\n')
    

    for s in sent_tokens[:-1]:
        words = word_tokenize(s)
        avg = str(sum(len(word)for word in words)/len(words))
        count = str(counter)    
        
        file.write('\t\t\t\t"avg":'+avg+',\n')
        file.write('\t\t\t\t"id":' + count + ',\n')
        file.write('\t\t\t\t"text":"'+s.encode("utf-8")+'"\n\t\t\t},\n\t\t\t{\n')
        
        counter += 1

    for s in sent_tokens[-1:]:
        words = word_tokenize(s)
        avg = str(sum(len(word)for word in words)/len(words))
        count = str(counter)
        file.write('\t\t\t\t"avg":'+avg+',\n')
        file.write('\t\t\t\t"id":' + count + ',\n')
        file.write('\t\t\t\t"text":"'+s.encode("utf-8")+'"\n\t\t\t}\n')
                    
        

    file.write("\t\t]\n\t}\n}")
    
   
    pass


       
        
