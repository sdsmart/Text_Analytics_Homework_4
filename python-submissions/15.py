


from __future__ import division

import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize


# In[3]:

nltk.download()



with codecs.open("twitter.txt", encoding='utf-8') as f:
    # Your code here
    raw = f.read()
    sents = nltk.sent_tokenize(raw)



import csv



#question 1
#problems: contain "" in the output and can not make each sentence in one cell
with codecs.open("twitter.txt", encoding='utf-8') as f:
    # Your code here
    raw = f.read()
    sents = nltk.sent_tokenize(raw)
    with codecs.open("output1.csv", 'w',) as p:
        writer = csv.writer(p, delimiter=' ')
        for i in xrange(len(sents)):
            sents[i] = sents[i].replace('\n',' ')
            words = word_tokenize(sents[i])
            num_char = 0 #to compute all number of charaters in all words
            for j in words:
                num_char += len(j)
            ave_word_size = num_char/len(words)
            row = u'%s'%i + u'þ' + sents[i] + u'þ' + u'%s'%ave_word_size
            row = row.encode('utf-8') #[s.encode('utf-8') for s in row]
            row = ''.join(row)
            writer.writerows([row])




#question 2
with codecs.open("twitter.txt", encoding='utf-8') as f:
    # Your code here
    raw = f.read()
    sents = nltk.sent_tokenize(raw)
    p = open("output2.xml", 'w')
    p.write('<document>\n')
    p.write(' '+'<sentences>\n')
    for i in xrange(len(sents)):
        p.write(' '+'<sentence id=\"{}\">\n'.format(i))
        sents[i] = sents[i].replace('\n',' ')
        row = [s.encode('utf-8') for s in sents[i]]
        row = ''.join(row)
        p.write('  '+'<text>{}</text>\n'.format(row))
        words = word_tokenize(sents[i])
        num_char = 0 #to compute all number of charaters in all words
        for j in words:
            num_char += len(j)
        ave_word_size = num_char/len(words)
        p.write('  '+'<avg>{}</avg>\n'.format(float(ave_word_size)))
        p.write('  '+'</sentence>\n')
    p.write(' '+'</sentences>\n')
    p.write('</document>\n')
    p.close()


import xmltodict, json


#question 3
import xml.etree.ElementTree as ET

tree = ET.parse('output2.xml')
root = tree.getroot()
sentences = root[0]

with codecs.open('data.json', 'w', encoding='utf-8') as f:
    feeds = {"documents":{"sentences":[]}}
    for i in xrange(len(sentences)):
        entry = {'avg':sentences[i][1].text, 'id':sentences[i].attrib['id'], 'text':sentences[i][0].text}
        feeds["documents"]["sentences"].append(entry)
    json.dump(feeds,f)
    

