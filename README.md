About This Repository
=====================
This homework was assigned to me in my Text Analytics class at the University of Oklahoma.

The project is about calculating several files and analyzing similarities between them based on the textual data.

My Approach
-----------
I analyzed the 16 files given in the assignment using one python script that
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

NOTES
-----
The python script is written in python 3.
I used glob to grab the all the .py files in a hard coded directory name.
I used subprocess to store command output within a script.

Run Instructions
----------------
Run the diff.py script in the same directory as the python-submissions folder.