#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division

import codecs

import json

import nltk
import csv

from nltk import sent_tokenize
from nltk import word_tokenize



raw = open('twitter.txt').read().decode('utf-8')
tokens = sent_tokenize(raw)
myList = []
lineCount = 0

for sentence in tokens:
	if not sentence.strip():
		continue
	else:
		words = nltk.word_tokenize(sentence)
		lengthWords = 0
		for word in words:
			if word != '.' or word != ',' or word != '?' or word != '1' or word != ':':
				lengthWords += len(word)
		avgWordLength = lengthWords / len(words)
		lineCount+=1
		myList.append({'Sentence Number': lineCount, 'Sentence': sentence.encode("ascii", "ignore"), 'Avg. Word Length' : avgWordLength})

fieldnames = ['Sentence Number', 'Sentence', 'Avg. Word Length']
test_file = open('twitter_analysis.csv', 'wb')
csvwriter = csv.DictWriter(test_file, delimiter='\xfe', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in myList:
	csvwriter.writerow(row)
test_file.close()


reader = csv.reader(open('twitter_analysis.csv'), delimiter='\xfe')
f = open('twitterXml.xml', 'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>')
f.write('<document>')
f.write(' ' + '<sentences>')
for row in reader:
	f.write(' ' + '<sentence id ="' + row[0] + '">')
	f.write('   ' + '<text>' + row[1] + '</text>')
	f.write('   ' + '<avg>' + row[2] + '</avg>')
	f.write(' ' + '</sentence>')      

f.write(' ' + '</sentences>')      	
f.write('</document>')
f.close()


pass
