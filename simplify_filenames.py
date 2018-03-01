"""
By Brian Tomasik
1 Mar. 2018

This program simplifies all the file names in the current directory (where the Python program is located) to remove non-alphanumeric characters and replace spaces with underscores. The goal is to make the file names nicer to work with on the command line or in url paths.

Some code is taken from https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
"""

import os
import unicodedata
import re

def run():
	print "WARNING: This program will rename the files in the current directory. Are you sure you want to continue? Enter 'y' if yes. Enter anything else to abort."
	answer = raw_input()
	if answer is 'y':
		for item in os.listdir(u'.'): # listdir's path has to be unicode in order to get unicode file names
			if os.path.isfile(item) and not item.startswith('.') and "simplify_filenames.py" not in item:
				filename, extension = os.path.splitext(item)
				renamed_filename = unicodedata.normalize('NFKD',filename).encode('ascii', 'ignore')
				renamed_filename = re.sub('[^\w\s-]', '', renamed_filename)
				renamed_filename = re.sub('[-\s]+', '_', renamed_filename)
				renamed_filename_with_extension = renamed_filename + extension
				#print "Renaming to {}".format(renamed_filename_with_extension)
				os.rename(item, renamed_filename_with_extension)
		print "Done."
	else:
		print "Program aborted."

if __name__ == "__main__":
	run()
