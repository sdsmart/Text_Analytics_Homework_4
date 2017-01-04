


from __future__ import division

import codecs

import json

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

import re

FILE_NAME = "twitter"
SEP = "þ"


# get the info about all of the sentences given the Twitter (or any) txt
def get_sentence_info(text):
	sents_unclean = sent_tokenize(text) # get sentences
	sents = [sent.replace('\n',' ') for sent in sents_unclean] #remove all newline chars in each sentence
	tokenized_sents = [word_tokenize(sent) for sent in sents] #split each sentence into words
	avg_word_size = [sum(len(w) for w in sent)/len(sent) for sent in tokenized_sents]

	return [sents, avg_word_size]


# part 1: creates a csv from a text
def create_sentence_csv(text):

	sents, avg_word_size = get_sentence_info(text)

	# create the content string for the .csv file
	csv_string = ""
	for i in range(0, len(sents)):
		csv_string += str(i + 1) + SEP + sents[i] + SEP + str(avg_word_size[i]) + "\n"

	# print the csv to the console
	print(csv_string)


	# create the file and populate
	with codecs.open(FILE_NAME + ".csv", 'w', encoding='utf-8') as f:
		f.write(csv_string)
		print(FILE_NAME + '.csv successfully created')
		pass


# add a line of xml to the current xml
# nt is number of tabs
def add_xml_line(xml, nt, line):
	xml += "\t" * nt + line 
	if line != "</document>":
		xml += '\n'
	return xml

# part 2: create an xml file from the text
def create_sentence_xml(text):
	sents, avg_word_size = get_sentence_info(text)

	xml_string = ""
	xml_string = add_xml_line(xml_string, 0, "<document>")	
	xml_string = add_xml_line(xml_string, 1, "<sentences>")	

	# loop through all the sentences to create the xml
	for i in range(0, len(sents)):
		xml_string = add_xml_line(xml_string, 2, "<sentence id = " + str(i) + ">")
		xml_string = add_xml_line(xml_string, 3, "<text>" + sents[i] + "</text>")	
		xml_string = add_xml_line(xml_string, 3, "<avg>" + str(avg_word_size[i]) + "</avg>")	
		xml_string = add_xml_line(xml_string, 2, "</sentence>")

	xml_string = add_xml_line(xml_string, 1, "</sentences>")	
	xml_string = add_xml_line(xml_string, 0, "</document>")	

	print(xml_string)

	# create the file and populate
	with codecs.open(FILE_NAME + ".xml", 'w', encoding='utf-8') as f:
		f.write(xml_string)
		print(FILE_NAME + '.xml successfully created')
		pass


# method to "tokenize" xml into tags and values between tags
# I don't *think* I can tokenize xml with regex since xml is not a regular language
def xml_tokenize(xml):
	xml_tokens = []
	token = ""

	# loop through xml and find full "tokens"
	for char in xml:
		if char == ">":
			token+=">"
			xml_tokens.append(token)
			token = ""
		elif char == "<" and len(token) > 0:
			xml_tokens.append(token)
			token = "<"
		else:
			token += char
	xml_tokens.append(token)

	#remove any tokens that are only whitespace
	return [x for x in xml_tokens if len(x.replace("\n",'').replace("\t",''))>0] 

# check if a unicode string is a number using a try/except
def unicode_is_num(str):
	try:
		float(str)
	except ValueError:
		return False
	return True

# helper method for Part 3
# recursive method for parsing xml and creating json, trating the xml_tokens list as a queue
# definitely not as generalized as I would like it; hoping to improve on this if we ever have a similar assignment	
def xml_to_json_inside(json, xml_tokens, level, sent_num=0):
	# pattern for any start tag
	start_tag_pattern = re.compile(r'^<[a-z,0-9,\s,=]+>$')

	# the tag-- "document", "avg", ect
	tag = ""
	
	# pattern for end tag-- will be filed in once tag is known
	end_tag_pattern = "" 


	if start_tag_pattern.match(xml_tokens[0]):

		# if the first token is a tag, find the name of the tag
		whole_tag = xml_tokens.pop(0)
		tag = whole_tag.replace("<", "").replace(">","").split()[0] #just get the tag name

		# find the id of the sentences
		if tag == "sentence":
			sent_num = whole_tag[15:-1]

		# create the pattern for the end tag
		pattern = r'^</'+ tag + '>$'
		end_tag_pattern = re.compile(pattern)

		# add a new line with necessary tabs
		json += "\n" + "\t"*level

		# each sentence line only has brackets 
		if level != 3:
			json += "\"" + tag + "\":"
		# the "sentences" line uses square brackets
		if level == 2:
			json += "[" 
		elif level < 4:
			json += "{" 
	else:
		print("Possible error in XML")
	
	# find each outer level tag within this tag 
	list_count = 0
	while len(xml_tokens) > 0 and not end_tag_pattern.match(xml_tokens[0]):
		# add a comma if there is already 1+ thing in list
		if(list_count > 0):
			json += ","

		# if find another starting tag, repeat inside recursively
		if start_tag_pattern.match(xml_tokens[0]):
			json, xml_tokens = xml_to_json_inside(json, xml_tokens, level+1, sent_num)

		# otherwise, it is the value of an attribute
		else:
			val = xml_tokens.pop(0)

			# put quotes around strings but not numbers
			if unicode_is_num(val):
				json += " " + val
			else:
				json += " \"" + val + "\""

		list_count += 1

	# id goes after text tag in json
	if(tag == "text"):
	  	json += ",\n" + level*"\t" + "\"id:\" " + str(sent_num)

	# if there are still tokens left...
	if len(xml_tokens) > 0:
		# if we have found the end tag, add closing brackets
		if level < 4 and end_tag_pattern.match(xml_tokens[0]):
			if level == 2:
				json += "\n" + "\t"*level +"]"
			else:
				json += "\n" + "\t"*level +"}"

		xml_tokens.pop(0)

	return [json, xml_tokens]


#part 3: creates json from the sentences xml
def create_sentence_json(xml):

	json_string = ""
	xml_tokens = xml_tokenize(xml) #get all the tags and values in a list
	json_string = "{" + str(xml_to_json_inside(json_string, xml_tokens, 1)[0]) + "\n}" # create json

	print(json_string)



	with codecs.open(FILE_NAME + ".json", 'w', encoding='utf-8') as f:
		f.write(json_string)
		print(FILE_NAME + '.json successfully created')
		return FILE_NAME + ".json"
		pass

	

# reading the txt file
with codecs.open(FILE_NAME + ".txt", encoding='utf-8') as f:
	
	text = f.read()
	csv_file_name = create_sentence_csv(text)
	create_sentence_xml(text)
	pass

# reading the xml file
with codecs.open(FILE_NAME + ".xml", encoding='utf-8') as f:
	xml = f.read()
	create_sentence_json(xml)
	pass
