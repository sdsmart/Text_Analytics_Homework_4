Text Simmilarity Analyzer
-------------------------
This project is about processing several documents and analyzing similarities between them based on the textual data.

### Run Instructions
Run the diff.py script. This script should output the analysis of the documents to the terminal.

### Discussion / Explanation
I analyzed the 16 files in the documents folder using one python script that
utilizes the diff linux command.

To determine the similarity percentage, I counted the total number of changes
required to transform file 1 into file 2 (for all file pairs) and divided that
by the total number of lines contained in both files. These changes are based on
line differences.

This results in: similarity percentage = required changes / maximum possible changes * 100

I then used a dictionary with keys being a string identifying the files being compared
and values being the similarity percentage.

The script then outputs these key-value pairs in order of similarity percentage as
specified by the assignment requirements.