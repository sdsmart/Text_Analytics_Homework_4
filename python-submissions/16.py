#!/usr/bin/python
# coding=utf-8


from __future__ import division

import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize


with codecs.open("twitter.txt", encoding='utf-8') as f:

    #output strings
    csvString = ""
    xmlString = ""
    jsonString = ""

    #split input file by periods, creating "sentences"
    sentence_list = sent_tokenize(f.read())
 
    sentence_number = 0
    word_count = 0
    character_count = 0

    #iterate over "sentences" of input
    for sentence in sentence_list:

        #replace spurious newlines with a space
        sentence = sentence.replace("\n", " ")

        word_count = 0
        character_count = 0

        #iterate over "words" of sentence
        for word in word_tokenize(sentence):
    
            #update variables for average word size calculation
            word_count += 1
            character_count += len(word)

        #add info to csv output string
        csvString += '{0}þ"{1}"þ'.format(sentence_number, sentence)
        csvString += '{:.6f}'.format(character_count/word_count)
        csvString += "\n"

        sentence_number += 1
    #csv string done

    #xml string begin
    xmlString += "<document>\n"
    xmlString += "\t<sentences>\n"

    #split csv string by newline characters
    csv_lines = csvString.splitlines()

    #iterate over lines of csv string
    for csv_line in csv_lines:

        #split line by thorn character
        line_list = csv_line.split('þ')

        #add info to xml output string
        xmlString += "\t\t<sentence id=\""
        xmlString += line_list[0]
        xmlString += "\">\n"
        xmlString += "\t\t\t<text>"
        xmlString += line_list[1][1:-1]
        xmlString += "</text>\n"
        xmlString += "\t\t\t<avg>"
        xmlString += line_list[2]
        xmlString += "</avg>\n"
        xmlString += "\t\t</sentence>\n"

    xmlString += "\t</sentences>\n"
    xmlString += "</document>"     
    #xml string done

    #json string begin
    #split xml string by sentence closing tag
    xml_elements = xmlString.split("</sentence>")

    first_element = 0
    json_text = ""
    json_avg = ""
    json_id = ""

    #iterate over sentence elements
    for xml_element in xml_elements:

        #split sentence element by newline characters
        element_lines = xml_element.splitlines()

        #iterate over lines of sentence element
        for element_line in element_lines:

            #remove formatting whitespace
            element_line = element_line.strip()

            #outer document case
            if "<document>" in element_line:
            
                jsonString += "{\n"
                jsonString += "\t\"documents\": {\n"
            
            #document close case
            if "</document>" in element_line:

                jsonString += "}\n"

            #sentences case
            if "<sentences>" in element_line:
    
                jsonString += "\t\t\"sentences\": [\n"
                
            #sentences close case
            if "</sentences>" in element_line:
    
                jsonString += "\n\t\t]\n"
                jsonString += "\t}\n"

            #beginning of new sentence element case
            if "<sentence " in element_line:

                #as long as this isn't the first element, add comma to end of previous element
                if first_element == 1:
                    
                    jsonString += ",\n"
                    
                else: 
            
                    first_element = 1

                #extract id # from attribute of sentence element
                json_id = element_line[14:element_line.index('>') - 1]

            #text case
            if "<text>" in element_line:

                #extract text from text element
                json_text = element_line[6:-7]
    
            #avg case
            if "<avg>" in element_line:

                #extract text from avg element
                json_avg = element_line[5:-6]
    
                #no more info in sentence element
                #add info to json output string
                jsonString += "\t\t\t{\n"
                jsonString += "\t\t\t\t\"text\": \""
                jsonString += json_text                
                jsonString += "\",\n"
                jsonString += "\t\t\t\t\"avg\": "
                jsonString += json_avg
                jsonString += ",\n"
                jsonString += "\t\t\t\t\"id\": "
                jsonString += json_id
                jsonString += "\n"
                jsonString += "\t\t\t}"
    #json string done
  
    #print output strings
    print(csvString)
    print(xmlString)   
    print(jsonString)

