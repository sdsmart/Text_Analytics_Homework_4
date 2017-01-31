

from __future__ import division

import codecs
import json
import re

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize



def avg_wc(sentence):
    letter_size = 0
    no_of_words = 0
    word = word_tokenize(sentence)
    no_of_words = len(word)
    for w in word:
        letter_size += len(w)
    return letter_size/no_of_words



with codecs.open("twitter.txt", encoding='utf-8') as f: #Decoding ASAP as per the Unicode Sandwich !!
    text = f.read()
    sentences = sent_tokenize(text)
    


    sentences = [re.sub(u'\n',' ',sent) for sent in sentences]
    average_word_count = [avg_wc(sent) for sent in sentences]
    
#appending thorn and the line number to the sentence

    new_sentences = [unicode(i)+u'þ"'+sent +u'"þ' for i,sent in enumerate(sentences)]
    i = 0
    while i<len(average_word_count):
        new_sentences[i] = new_sentences[i]+unicode(average_word_count[i])
        i+=1
        
#Creamy Unicode Ends
for each_line in new_sentences:
    each_line = each_line.encode('utf-8') #Encoding as late as possible
    print each_line
  
    
#Problem 2:

#Creating a structure for the xml and looping through it

header = u'<document>\n\t<sentences>'
header = header.encode('utf-8')
print header

#a tuple containing id,sentences and average word count

data_tuple = [[0]*3 for i in range(0,len(sentences))]
for i in range(0,len(sentences)):
    data_tuple[i][0] = i
    data_tuple[i][1] = sentences[i]
    data_tuple[i][2] = (average_word_count[i])
container = u''
for i in range(0,len(data_tuple)):
    container += u'\t\t<sentence id ="'+unicode(data_tuple[i][0])+u'">\n\t\t\t<text>'+unicode(data_tuple[i][1])+u'</text>\n\t\t\t<avg>'+unicode(int(data_tuple[i][2]))+u'</avg>\n\t\t</sentence>\n'
container = container.encode('utf-8')
print container

footer = u'\t</sentences>\n<documents>'
footer = footer.encode('utf-8')
print footer

#Problem 3

#making use of the inbuilt json.dumps function to create the structure

json_struct = {"documents":{"sentences":[{"text":text,"avg":avg,"id":ids} for ids,text,avg in data_tuple]}}
print json.dumps(json_struct,indent = 4)








    

  


