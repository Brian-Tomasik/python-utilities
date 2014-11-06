"""
By Brian Tomasik
23 May 2014

This program changes the anchors for the sections and table of contents of an HTML file from using section numbers to using the section title as the anchor for the section. The formatting this program assumes is fairly specific to the task for which I used it.
"""

import re
import sys
import pdb

def ConvertAnchorsToText(input,outfile):
	sectionNamesSoFar = set()
	with open(input,'r') as file:
		with open(outfile,'w') as output:
			for line in file:
				lineToOutput = line
				
				# Is this a table-of-contents line?
				tableOfContentsLine = re.match(".*#section\d+(\.\d+)?\">\d+\.(\d+\.)? ([^<]+)<.*",line)
				if tableOfContentsLine:
					print "Table-of-contents line, originally:"
					print line ,
					sectionName = ProcessSectionNameIntoAnchor(tableOfContentsLine.group(3))
					if sectionName in sectionNamesSoFar:
						raise Exception("Two section names with same string. Fix manually.")
					sectionNamesSoFar.add(sectionName)
					lineWithNewAnchor = re.sub("section\d+(\.\d+)?",sectionName,line)
					lineWithoutNumber = re.sub(">\d+\.(\d+\.)? ",">",lineWithNewAnchor)
					lineToOutput = lineWithoutNumber
					print "Changed to:"
					print lineToOutput
				
				# Is this an in-body section line?
				else:
					bodySectionLine = re.match(".*section\d+(\.\d+)?\">([^<]+)<.*",line)
					if bodySectionLine:
						print "Body-section line, originally:"
						print line ,
						sectionName = ProcessSectionNameIntoAnchor(bodySectionLine.group(2))
						lineToOutput = re.sub("section\d+(\.\d+)?\">",sectionName + "\">",line)
						print "Changed to:"
						print lineToOutput					
				
				output.write(lineToOutput)

def ProcessSectionNameIntoAnchor(string):
	OnlyLettersNumbersAndSpaces = re.sub("[^A-Za-z0-9 ]","",string)
	SpacesToUnderscores = re.sub(" ","_",OnlyLettersNumbersAndSpaces)
	return SpacesToUnderscores
					
if __name__ == '__main__':
	input = sys.argv[1] # input HTML file
	outfile = sys.argv[2] # output with anchors converted to text
	ConvertAnchorsToText(input,outfile)