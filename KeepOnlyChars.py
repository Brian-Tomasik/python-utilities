"""
By Brian Tomasik
3 May 2014

This program takes an input file and prints out just the alphabetical (A-Z and a-z) characters in word blocks, one word per line. All non-alphabetical characters are taken to be word separators. The original goal was to get a clean set of words in order to diff two HTML files without differences in HTML formatting producing differences in a text-file diff. Of course, this script can be used for other purposes as well.
"""

import re
import sys

input = sys.argv[1] # the file to process
outfile = sys.argv[2] # the name of the file where to dump its words
wordsPrinted = 0

with open(input,'r') as file:
	with open(outfile,'w') as output:
		text = file.read().lower()
		alphabeticalWords = re.split("[^A-Za-z]",text) # split on anything not an alphabetical character
		for word in alphabeticalWords:
			if word != "":
				wordsPrinted += 1
				output.write(word + '\n')
				if wordsPrinted % 500 == 0:
					print "Printed {0} words".format(wordsPrinted)