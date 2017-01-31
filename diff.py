#!/usr/bin/env python3

############################
# Name: Stephen Smart      #
# ID: 113851356            #
############################

# Imports
import glob
import subprocess
import operator

# File organization variables
base_dir = 'documents/'
file_names = glob.glob(base_dir + '*.py');
# String containing the diff command output
output = ''
# Total number of changes needed to convert file 1 to file 2
num_changes = 0;
# Total number of lines in both files being compared
num_lines = 0
# Dictionary to store the ranks of all the file pairs
file_pairs = {}

# Looping through each pair of files
for i, f1_name in enumerate(file_names):

	# Ignoring the files that have already been compared
	for f2_name in file_names[i:]:

		# If the file is the same, the comparison is trivial so it is ignored
		if f1_name != f2_name:

			# Running the diff command in terminal and saving the output to a pythong string
			# decoded using utf-8
			cmd = ['diff', '-u', '-b', f1_name, f2_name]
			output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

			# Splitting the diff output by lines (ignoring the first 3)
			lines = output.split('\n')[3:]

			# Opening and reading the files to calculate the total number of lines
			f1 = open(f1_name)
			f2 = open(f2_name)
			num_lines = len(f1.read().split('\n')) + len(f2.read().split('\n'))

			# Calculating the total number of changes required to convert file 1 to file 2
			for l in lines:
				if l.startswith('+') or l.startswith('-'):
					num_changes += 1

			# Calculating the similarity percentage
			similarity = round((100 * (1 - (num_changes / num_lines))), 2)

			# Reseting the num_changes value back to 0
			num_changes = 0

			# Formatting the pair key for the ranks dictionary
			pair_key = f1_name[len(base_dir):] + ' compared with ' + f2_name[len(base_dir):]

			# Adding the pair and similarity percentage to the ranks dictionary
			file_pairs[pair_key] = similarity

# Sorting the file pairs by similarity
sorted_file_pairs = sorted(file_pairs.items(), key=operator.itemgetter(1), reverse=True)

# Printing sorted file pairs
for i, f_pair in enumerate(sorted_file_pairs):
	print(f_pair[0])
	print('similarity: ' + str(f_pair[1]))
	print('rank: ' + str(i+1) + '\n')
