"""
This program checks for overlapping sequences of words in two files, to see if one chunk of text is copied from the other. Enter the paths to the two files in the variables input1 and input2, and then set numConsecutiveWords, which is how many consecutive words have to be in common before we print out that sequence as overlapping. The output file will be outfileprefix + numConsecutiveWords + ".txt"
"""

input1 = 'doc1.txt'
input2 = 'doc2.txt'
numConsecutiveWords = 5
outfileprefix = 'output'

with open(input1,'r') as file1:
	with open(input2,'r') as file2:
		with open(outfileprefix + str(numConsecutiveWords) + '.txt','w') as output:
			words1 = file1.read().lower().split()
			words2 = file2.read().lower().split()
			for i in range(len(words1)):
				for j in range(len(words2)):
					if words1[i:i+numConsecutiveWords] == words2[j:j+numConsecutiveWords] and len(words1[i:i+numConsecutiveWords]) >= numConsecutiveWords:
						outstring = ' '.join(words1[i:i+numConsecutiveWords])
						print outstring
						output.write(outstring + '\n')