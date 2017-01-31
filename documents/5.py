

from __future__ import division

import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

import re

def find_avg_word_len(sent):
	total_words = len(sent)
	sum = 0
	for word in sent:
		sum = sum + len(word)
	return sum/total_words

def make_csv(text):
    #split into sentences
    text = sent_tokenize(text)
	
    f = open('twitter_text.csv', 'w')

    # for each sentence, make a list "parts" containing the sentence index,
       # sentence text, and average word length
    for index, item in enumerate(text):
        # replace newlines in each item
        item = item.replace('\n', ' ')
        # split into words
        word_list = word_tokenize(item)

        # find avg word len
        avg_word_len = find_avg_word_len(word_list)

        # write to file w thorns
        line = item.encode('utf-8')
        parts = [str(index), line, str(avg_word_len)]

        #print 'þ'.join(parts)
        f.write('þ'.join(parts))
        f.write('\n')

    f.close()

def convert_to_xml():
    f = open('twitter_text.xml', 'w')
    f.write('<document>\n')
    f.write('\t<sentences>\n')

    # process the text in the csv file
    csvfile = open('twitter_text.csv')
    for line in csvfile:
        fields = re.split('þ', line)
        fields[2] = (fields[2]).replace('\n', ' ') # added this line bc every average has a \n attached to it
        f.write('\t\t<sentence id ="' + fields[0] + '">'+ "\n")
        f.write('\t\t\t<text>' + fields[1] + '</text>\n')
        f.write('\t\t\t<avg>' + fields[2] + '</avg>\n')
        f.write('\t\t</sentence>\n')

    f.write('\t</sentences>\n')
    f.write('</document>')

    csvfile.close()
    f.close()

def convert_to_json():
    
    f = open('twitter_text.json', 'w') # replace w json
    f.write('{\n')
    f.write('\t"documents": {\n')
    f.write('\t\t"sentences": [\n\t\t\t{\n')

    # process text in xml file
    # kinda janky
    # actually this won't work--I need to make a stack in order to handle this!
    xmlfile = open('twitter_text.xml')
    for line in xmlfile:
        line = line.replace('<', 'þ')
        line = line.replace('>', 'þ')
        line = line.replace('\t', '')
        fields = re.split('þ', line)
        # write info into json in the right order
        # this is unfinished but you get the idea...


    # end-of-doc brackets


# -------main program starts here--------
with codecs.open("twitter.txt", encoding='utf-8') as f:
    text = f.read()

    make_csv(text)

# open the csv file and covert it to xml
convert_to_xml()

# open the xml file and convert to json
convert_to_json()