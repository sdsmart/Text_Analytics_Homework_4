#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division

import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

import re, pprint, os, csv


# Open twitter file and read in
with codecs.open("twitter.txt", encoding='utf-8') as f:
  sample = f.read()

#Tokenize the sample into sentences
sentences = sent_tokenize(sample)
tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

# Initialize count variable and create a unicode variable for quotation marks
count = 0
q = u'\u0022'

# Create the csv file.
delim = b'\xc3\xbe'.decode() #convert the binary thorn symbol to unicode.
with codecs.open('x.csv', 'w', encoding="utf8") as csvfile:
  wr = csv.writer(csvfile,delimiter = delim, quoting=csv.QUOTE_MINIMAL, quotechar = "'")
  count = 0
  for sentence in sentences:
    text = sentence.replace('\n', ' ').replace('\r', ''); # replace the newline and carriage returns
    avg_word_len = repr(len(text)/len(word_tokenize(text))) # Calculate the avg word length per sentence
    fmt_avg_word_len = "{0:.6f}".format(float(avg_word_len)) # Format the avg word length to 6 decimals
    wr.writerow([count, q + text + q, fmt_avg_word_len]) # Write row with quotes
    count += 1 # Increment the counter
csvfile.close()

# Create the xml file.
xmlFile = codecs.open('x.xml', 'w', encoding="utf8") # Open the unicode file in write mode.
csvData = csv.reader(codecs.open('x.csv', 'r', encoding="utf8"),delimiter = delim) # Open the unicode csv in read mode.

#Create xml file header and initial non-looping elements
xmlFile.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
xmlFile.write('<document>' )
xmlFile.write('\t' + '<sentences>')
for row in csvData: # for each row in the cvs file, create the sentence element.
  xmlFile.write('\t\t' + '<sentence id="' + row[0] + '">')
  xmlFile.write('\t\t\t' + '<text>' + row[1] + '</text>')
  xmlFile.write('\t\t\t' + '<avg>' + row[2] + '</avg>')
  xmlFile.write('\t\t' + '</sentence>')

# Close the initial elements
xmlFile.write('\t' + '</sentences>')
xmlFile.write('\t' + '</document>')
xmlFile.close(); # Close the xmlFile.

from xml.dom.minidom import parse
import xml.dom.minidom

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("x.xml")
collection = DOMTree.documentElement

# Create the json file from the xml file
jsonFile = codecs.open('j.json', 'w', encoding="utf8") # Open the unicode file in write mode.
jsonCount=0

#Write the header to the json file
jsonFile.write('{\n' )
jsonFile.write('\t\"documents\":{\n')
jsonFile.write('\t\t\"sentences\":[\n')

# Get all the sentences in the collection
sentences = collection.getElementsByTagName("sentence")

# Print detail of each movie.
for sentence in sentences:
  jsonFile.write('\t\t\t{\n')
  jsonFile.write('\t\t\t\t\"avg\":' + sentence.getElementsByTagName('avg')[0].childNodes[0].data + ',\n')
  if sentence.hasAttribute("id"):
    jsonFile.write('\t\t\t\t\"id\":' + sentence.getAttribute("id") + ',\n')
  jsonFile.write('\t\t\t\t\"text\":' + sentence.getElementsByTagName('text')[0].childNodes[0].data + '\n')
  jsonCount += 1
  if jsonCount == count: # If last record close data element without comma
    jsonFile.write('\t\t\t}\n')
  else:  # else need a comma to format json properly.
    jsonFile.write('\t\t\t},\n')    


   #print "Type: %s" % type.childNodes[0].data   
   
   
   #format = movie.getElementsByTagName('format')[0]
   #print "Format: %s" % format.childNodes[0].data
   #rating = movie.getElementsByTagName('rating')[0]
   #print "Rating: %s" % rating.childNodes[0].data
   #description = movie.getElementsByTagName('description')[0]
   #print "Description: %s" % description.childNodes[0].data

# Close the json header tags.
jsonFile.write('\t\t]\n')   
jsonFile.write('\t}\n' )
jsonFile.write('}\n')
 
jsonFile.close(); # Close the jsonFile.
    
