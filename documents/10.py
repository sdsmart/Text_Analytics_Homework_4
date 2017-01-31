#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/


from __future__ import division
import codecs
import json
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
import xml.etree.ElementTree as ET

# converts a list of sentences generated from sent_tokenize
# into a csv format with þ (thorn) as the delimeter
def create_csv_format(sentences):
    result_string = ''

    sent_num = 1
    for sent in sentences:
        sent = sent.replace('\n', ' ')
        words = word_tokenize(sent)

        char_total = 0
        for w in words:
            char_total += len(w)
        avg_word_size = char_total / len(words)

        result_string += '{0} þ {1} þ {2}\n'.format(sent_num, sent, avg_word_size)

        sent_num += 1

    return result_string

# converts a string in csv format into xml format
def create_xml_format(csv):
    csv_rows = [x for x in csv.split('\n') if x]

    result_string = '<document>\n'
    result_string += '\t<sentences>\n'

    for row in csv_rows:
        row = row.replace(' ', '').split('þ')
        result_string += '\t\t<sentence id=\"{0}\">\n'.format(row[0])
        result_string += '\t\t\t<text>{0}</text>\n'.format(row[1])
        result_string += '\t\t\t<avg>{0}</avg>\n'.format(row[2])
        result_string += '\t\t</sentence>\n'

    result_string += '\t</sentences>\n'
    result_string += '</document>\n'

    return result_string

# converts a string from xml format to json format
# NOTE: this function in particularly is a little sloppy. I found it actually pretty tricky
# to create a smooth transition from xml to json
def create_json_format(xml):
    root = ET.fromstring(xml)

    result_string = '{\n'
    result_string += '\t\"document\": {\n'

    sentences = root[0]
    result_string += '\t\t\"sentences": [\n'
    counter = 0
    for sent in sentences:
        result_string += '\t\t\t{\n'
        result_string += '\t\t\t\t\"id\": \"{0}\":\n'.format(sent.attrib['id'])
        for data in sent:
            result_string += '\t\t\t\t\"{0}\": \"{1}\"\n'.format(data.tag, data.text)
        counter += 1
        if counter < len(sentences):
            result_string += '\t\t\t},\n'
        else:
            result_string += '\t\t\t}\n'
    result_string += '\t\t]\n'

    result_string += '\t}\n'
    result_string += '}'

    return result_string

# opening the twitter.txt file
with codecs.open("twitter.txt", encoding='utf-8') as f: 

    # generating a list of sentences from the twitter.txt file using sent_tokenize
    sentences = sent_tokenize(f.read())

    # converting the sentences to various formats
    csv_result = create_csv_format(sentences)
    xml_result = create_xml_format(csv_result)
    json_result = create_json_format(xml_result)

    # printing the sentences and associated data in the various formats
    print(csv_result)
    print(xml_result)
    print(json_result)
