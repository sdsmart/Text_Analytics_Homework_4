

# imports
from __future__ import division
import codecs # for utf-8
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

# file names
input_file = "twitter.txt"
output_csv = "sents.csv"
output_xml = "sents.xml"
output_json = "sents.json"

# þ
THORN = u'þ'

tos_text = ""
csv_out = ""
xml_out = ""
json_out = ""

# read in twitter text
with codecs.open(input_file, encoding='utf-8') as f:
    tos_text = f.read()
    f.close()
    pass

########### Question 1 ##############

# build csv data
sents = sent_tokenize(tos_text)
for s in sents:
    s_temp = s.strip()
    s_temp = s_temp.replace('\n', ' ')
    words = word_tokenize(s_temp)
    total = 0
    avg = 0
    for w in words:
        total = total + len(w)
    if w > 0:
        avg = total / len(words)
    csv_out = csv_out + str(sents.index(s)) + THORN + s_temp + THORN + str(avg) + '\n'
    
# write csv data
with codecs.open(output_csv, encoding='utf-8', mode='w') as f_out:
    f_out.write(csv_out)
    f_out.close()

########### Question 2 ##############

# build xml data
xml_out = '<document>\n\t<sentences>\n'
for s in sents:
    s_temp = s.strip()
    s_temp = s_temp.replace('\n', ' ')
    words = word_tokenize(s_temp)
    total = 0
    avg = 0
    for w in words:
        total = total + len(w)
    if w > 0:
        avg = total / len(words)
    xml_out = xml_out + "\t\t<sentence id=\"" + str(sents.index(s)) + "\">\n"
    xml_out = xml_out + "\t\t\t<text>" + s_temp + "</text>\n"
    xml_out = xml_out + "\t\t\t<avg>" + str(avg) + "</avg>\n\t\t</sentence>\n"

xml_out = xml_out + '\t</sentences>\n</document>'

# write xml data
with codecs.open(output_xml, encoding='utf-8', mode='w') as f_out:
    f_out.write(xml_out)
    f_out.close()


########### Question 3 ##############

# build json data
json_out = "{\n\t\"documents\": {\n\t\t\"sentences\": [\n"
for s in sents:
    s_temp = s.strip()
    s_temp = s_temp.replace('\n', ' ')
    words = word_tokenize(s_temp)
    total = 0
    avg = 0
    for w in words:
        total = total + len(w)
    if w > 0:
        avg = total / len(words)
    json_out = json_out + "\t\t\t{\n\t\t\t\t\"avg\": " + str(avg) + ",\n"
    json_out = json_out + "\t\t\t\t\"id\": " + str(sents.index(s)) + ",\n"
    json_out = json_out + "\t\t\t\t\"text\": \"" + s_temp + "\"\n\t\t\t},\n"

json_out = json_out[:len(json_out)-2] # cut off the last comma
json_out = json_out + "\n\t\t]\n\t}\n}"

# write json data
with codecs.open(output_json, encoding='utf-8', mode='w') as f_out:
    f_out.write(json_out)
    f_out.close()
