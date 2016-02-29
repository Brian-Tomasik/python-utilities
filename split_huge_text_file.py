"""
By Brian Tomasik
29 Feb. 2016

This program takes a huge (probably >2 GB) input text file and splits it into manageable chunks.
"""

import sys

def run():
	input = sys.argv[1] # input file, has to be in same folder as the .py program
	n_lines_per_chunk = 3000000
	input_filename_parts = input.split('.')

	with open(input,'rb') as file:
		cur_chunk_num = 0
		print "  now doing chunk %i" % cur_chunk_num
		lines_in_cur_file_so_far = 0
		cur_output_file = open(create_chunk_file_name_from_original_file_name_parts(input_filename_parts, cur_chunk_num), 'wb')
		for line in file:
			lines_in_cur_file_so_far += 1
			cur_output_file.write(line)		
			if lines_in_cur_file_so_far >= n_lines_per_chunk:
				cur_output_file.close()
				cur_chunk_num += 1
				print "  now doing chunk %i" % cur_chunk_num
				lines_in_cur_file_so_far = 0
				cur_output_file = open(create_chunk_file_name_from_original_file_name_parts(input_filename_parts, cur_chunk_num), 'wb')
		cur_output_file.close() # close the last file
		print "Done. :)"

def create_chunk_file_name_from_original_file_name_parts(input_filename_parts, chunk_num):
	return input_filename_parts[0] + "_part" + str(chunk_num) + "." + input_filename_parts[1]
		
if __name__ == "__main__":
	run()