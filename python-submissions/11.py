#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division

import codecs

import csv
import xml.etree.cElementTree as ET
import json

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
    # Your code here
    count = 0
    root = ET.Element("document")
    csv_file = open('twitter.csv', 'wb')
    sent_tokens= sent_tokenize(f.read())
    sents = ET.SubElement(root, "sentences")
    data = {}
    document = {}
    
    sentences = []
    
    for sent in sent_tokens:
        ET.SubElement(sents, "sentence id").text = str(iter)
        ET.SubElement(sents, "text").text = sent
        
        word_tot = 0
        if sent.rstrip():
            word_tokens= word_tokenize(sent)
            for words in word_tokens:
                word_tot += len(words)
                avg_length = word_tot/len(word_tokens)
                final_out =  str(count) + u"\u00FE" + sent+ u"\u00FE"  + str(avg_length)
                csv_write = csv.writer(csv_file,delimiter= '\xfe',quotechar = '"')
                row = []
        sentences.append({"sentence id" : count,
                         "text" : sent,"avg":avg_length})
        count +=1;
        row.append(final_out.strip().encode("utf-8"))#write to csv file
        ET.SubElement(sents, "avg").text = str(avg_length)

        
        data["sentences"] = sentences
        document["documents"] = data

        csv_write.writerow(row)
        tree = ET.ElementTree(root)
        tree.write("twitter.xml",encoding="utf-8", xml_declaration=True)#Write to xml file

    with open('twitterjson.txt', 'w') as outfile:
        json.dump(document, outfile,indent=2)#Write to json file


pass
