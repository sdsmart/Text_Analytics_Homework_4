

from __future__ import division

import codecs

import json
import csv

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

from xml.etree.ElementTree import ElementTree


###############################################  CSV
f = codecs.open('twitter.txt', 'r', 'utf-8') # Read in text from file
text = f.read()

a = nltk.word_tokenize(text) #tokenize text into words
tokenized_sentences=nltk.sent_tokenize(text) #tokenize text into sentences
tokenized_sentences[-1]='Solutions' # remove unwanted words from last sentence and end file where specified

f1=open("final-output.txt", "w+", encoding="utf-8") #open csv file

wt=open("twitter-output.csv", "w+", encoding="utf-8") #open csv file
writer = csv.writer(wt, delimiter='\xfe', quotechar="'")


index = 0
for sent in tokenized_sentences:  # loop through sentenses
    tokenized_words=nltk.word_tokenize(sent)
    numberofwords=len(tokenized_words)
    totallength = 0
    for word in tokenized_words:
        #print(len(word))
        totallength+=len(word)
    AverageWordSize = totallength/numberofwords # calculate average word size
    StripedSent= sent.replace('\n', ' ')
    print(index, "\"{}\"".format(StripedSent), "{:.6f}".format(AverageWordSize), file=f1) # print to output txt file 
    writer.writerows([[index, '\"{}\"'.format(StripedSent),"{:.6f}".format(AverageWordSize)]]) #print to csv file
    index+=1
    
wt.close() # close file
##################################################  XML
f = codecs.open('twitter.txt', 'r', 'utf-8') 
text = f.read() # Read in text from file

a = nltk.word_tokenize(text)
tokenized_sentences=nltk.sent_tokenize(text) #tokenize text into sentences
tokenized_sentences[-1]='Solutions' # remove unwanted words from last sentence and end file where specified

xmlwrite=open("twitter-output.xml", "w+", encoding="utf-8") #open xml file

xmlwrite.write('<document>')
xmlwrite.write('\n        <sentences>')
print('<document>', file=f1)                #print to file
print('\n        <sentences>', file=f1)
index = 0
for sent in tokenized_sentences:
    tokenized_words=nltk.word_tokenize(sent)   # loop through sentenses
    numberofwords=len(tokenized_words) # number of words in each sentence
    totallength = 0
    for word in tokenized_words:
        #print(len(word))
        totallength+=len(word) # sum of length of all words in each sentence
    AverageWordSize = totallength/numberofwords # calculate average word size
    StripedSent= sent.replace('\n', ' ')
    xmlwrite.write('\n                <sentence id=\"'+str(index)+'\">')#print to xml file with repective format
    xmlwrite.write('\n                        <text>'+StripedSent+'</text>') 
    xmlwrite.write('\n                        <avg>'+str("{:.0f}".format(AverageWordSize))+'</avg>')
    xmlwrite.write('\n                </sentence>')
    print('\n                <sentence id=\"'+str(index)+'\">', file=f1)
    print('\n                        <text>'+StripedSent+'</text>', file=f1)
    print('\n                        <avg>'+str("{:.0f}".format(AverageWordSize))+'</avg>', file=f1)
    print('\n                </sentence>', file=f1)
    index+=1

xmlwrite.write('\n        </sentences>')
xmlwrite.write('\n</document>')
print('\n        </sentences>', file=f1)
print('\n</document>', file=f1)
xmlwrite.close()  # close file

#################################################  JSON

tree = ElementTree().parse('twitter-output.xml') # parse out xml file into a tree
jsonwrite=open("twitter-output.json", "w+", encoding="utf-8") #open json file

jsonwrite.write('{')  # beging printing json format elements
jsonwrite.write('\n   \"documents\":{')
jsonwrite.write('\n        \"sentences": [')
print('{', file=f1)
print('\n   \"documents\":{', file=f1)
print('\n        \"sentences": [', file=f1)

i = 0
last = 0
for e in tree.iter('sentence'):  # find the last element in the file
    last +=1

for sent in tree.iter('sentence'):  # main loop
    
    if i != last-1:   #if not the last element
        jsonwrite.write('\n        {')
        jsonwrite.write('\n                \"text\": \"'+sent[0].text+'\",')
        jsonwrite.write('\n                \"avg\": \"'+sent[1].text+'\",')
        jsonwrite.write('\n                \"id\": ')
        jsonwrite.write(sent.get('id'))
        jsonwrite.write('\n        },')
        print('\n        {', file=f1)
        print('\n                \"text\": \"'+sent[0].text+'\",', file=f1)
        print('\n                \"avg\": \"'+sent[1].text+'\",', file=f1)
        print('\n                \"id\": ', file=f1)
        print(sent.get('id'), file=f1)
        print('\n        },', file=f1)
        i+=1
  
    else:  # if last element we need to print different closing bracket
        jsonwrite.write('\n        {')
        jsonwrite.write('\n                \"text\": \"'+sent[0].text+'\",')
        jsonwrite.write('\n                \"avg\": \"'+sent[1].text+'\",')
        jsonwrite.write('\n                \"id\": ')
        jsonwrite.write(sent.get('id'))
        jsonwrite.write('         }')
        print('\n        {', file=f1)
        print('\n                \"text\": \"'+sent[0].text+'\",', file=f1)
        print('\n                \"avg\": \"'+sent[1].text+'\",', file=f1)
        print('\n                \"id\": ', file=f1)
        print(sent.get('id'), file=f1)
        print('         }', file=f1)

jsonwrite.write('\n       ]')
jsonwrite.write('\n   }')
jsonwrite.write('\n}')
print('\n       ]', file=f1)
print('\n   }', file=f1)
print('\n}', file=f1)
jsonwrite.close()


#######output to one text file
f1.close() # close main output text file
