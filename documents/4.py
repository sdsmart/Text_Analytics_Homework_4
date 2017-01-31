

from __future__ import division

import codecs

import json

import nltk

import xmltodict

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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



# FIRST
with codecs.open("//Users//priyankapothineni//Desktop//assignment//twitter.txt", encoding='utf-8') as f:
    # Your code here
    def word_count(sentence):
        data = word_tokenize(sentence)
        word_count = len(data)
        sum=0
        for w in data:
            sum = sum+len(w)
        return (sum/word_count)

    l=f.read()
    l=l.replace("\n"," ")
    x=sent_tokenize(l)
    count=0
    result1=""
    for sentence in x:
        string=""
        # 1st output :D
        print count,"þ",sentence,"þ",word_count(sentence)
        count=count+1
f.close()


#SECOND
with codecs.open("//Users//priyankapothineni//Desktop//assignment//result1.txt", encoding='utf-8') as f:

    l=f.read().replace("\n"," ").encode('utf-8')
    l=l.split("þ")
    c=len(l)
    i=2
    while(i<c-1):
        l[i]=l[i].split(" ")
        l[i].pop(0)
        l[i].pop(2)
        l[i]
        i=i+2

    def idss(count):
        print"\t\t<sentence id=\"",l[count],"\">"

    def ids(count):
        print"\t\t<sentence id=\"",l[count][1],"\">"

    def text(count):
        print"\t\t\t\t\t<text>",l[count],"</text>"

    def avg(count):
        print"\t\t\t\t\t<avg>",l[count][0],"</avg>"
        print"\t\t</sentence>"


    def print_xml():
        id=0
        print"<document>"
        print"\t<sentences>"
        count =0
        while(count<len(l)-1):
            data = (count)%2

            if(count==0):
                idss(count)
            elif(data == 1):
                text(count)
            elif(data == 0):
                avg(count)
                ids(count)
            count = count+1
        if(count==len(l)-1):
            print"\t\t\t\t\t<avg>",l[count],"</avg>"
            print"\t\t</sentence>"
        print"\t</sentences>"
        print"</document>"

    # print_xml()
    f.close()


#THIRD
# with codecs.open("//Users//priyankapothineni//Desktop//assignment//myoutput2.xml", encoding='utf-8') as f:
#     d = xmltodict.parse(f.read())
#     r = json.dumps(d, indent=4)
#     print r
#     f.close()
