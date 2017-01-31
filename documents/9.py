#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division

import os, sys
import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

import csv
from lxml import etree as ET
import math

import xml.etree.ElementTree as XET
import xml.etree.cElementTree as CET

iter = 0
with codecs.open("twitter.txt", encoding='utf-8') as f:
    
   
    file = open("txtTocsv.csv", 'wb')

    root = ET.Element("document")
    doc = ET.SubElement(root, "sentences")
    ave_word_len = 0

    for sent in sent_tokenize(f.read()):
	sent = sent.replace("\n", " ")
	total_word_len = 0

	for word in word_tokenize(sent):
		total_word_len += len(word)
        ave_word_len = total_word_len/len(word_tokenize(sent))
	
	
	field = str(iter) + u"\u00FE" + '"' + sent + '"' + u"\u00FE" + str(ave_word_len)
	writer = csv.writer(file, delimiter = '\xfe', quotechar = '"')
	row = [] 
	row.append(field.strip().encode("utf-8"))
	writer.writerow(row)
	#iter += 1

	#csv print
        print field

	# Question 2: txt to xml        
        sentid = ET.SubElement(doc, "sentence", id=str(iter)) 
	txt = ET.SubElement(sentid, "text")
	txt.text = sent
	av = ET.SubElement(sentid, "avg")
	av.text = str(math.floor(ave_word_len))

	tree = ET.ElementTree(root)
	tree.write("xmlout.xml", method="xml", encoding="UTF-8", xml_declaration=False, pretty_print=True)
	iter += 1 	 

    #xml print
    xtree = XET.parse("xmlout.xml")
    xmlStr = XET.tostring(xtree.getroot(), encoding='utf-8', method='xml')
    print xmlStr




# Question 3: xml to jason
tree = CET.ElementTree(file="xmlout.xml")
root = tree.getroot()
id = -1
dict1 = []
dict2 = {"documents": {"sentences": dict1}};

for child in root:
    #print child.tag, child.attrib
    if child.tag == "sentences":
    	for step_child in child:
            #print step_child.tag, step_child.attrib
            step_children = step_child.getchildren()
            id = int((step_child.attrib).get('id'))
            dict3 = {}

            for schild in step_children:
            	#print "%s=%s" % (schild.tag, schild.text)
		if schild.tag == "avg":
                	dict3.update({schild.tag : float(schild.text)})
		else:
			dict3.update({schild.tag : schild.text})
                
		dict3.update({"id" : id})
            dict1.append(dict3)

#jason print
print json.dumps(dict2, sort_keys=True, indent=4)

#jason file write
out_jason = open("xmlTojason.json", "w")
json.dump(dict2, out_jason, indent=4)
out_jason.close()

