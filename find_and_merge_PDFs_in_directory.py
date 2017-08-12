"""
By Brian Tomasik
12 Aug. 2017

This program merges all the PDF files in a given directory (including subdirectories, subsubdirectories, etc.) into
a specified number of output PDF files.

This script requires PyPDF2. You can install it with the command:
  sudo pip install PyPDF2

Sample usage: To merge all PDFs in mywebsitedirectory/ into 5 PDF files, run:
  python merge_PDFs.py mywebsitedirectory 5
"""

import sys
import os
import math
from PyPDF2 import PdfFileMerger

def run():
    input_folder = sys.argv[1]  # input WordPress site-download folder (without any ending "/"), has to be in same folder as the .py program
    split_output_into_this_many_PDF_files = int(sys.argv[2])
    assert split_output_into_this_many_PDF_files >= 1, "split_output_into_this_many_PDF_files must be at least 1"

    all_PDF_files = []

    print "Getting a list of all PDF files...\n"
    for (path, dirs, files) in os.walk(input_folder):
        for file in files:
            if is_PDF_file(file):
                all_PDF_files.append(os.path.join(path, file))

    if len(all_PDF_files) == 0:
        print "WARNING: There are no PDFs to merge!"
        return

    print "Identifying PDFs that for some reason cause this program to crash...\n"
    TEMP_FILE = "temp_delete_me.pdf"
    PDF_files_to_use = []
    merger = PdfFileMerger()
    for file in all_PDF_files:
        try:
            with open(file, 'rb') as opened_file:
                merger.append(opened_file)
                with open(TEMP_FILE,'wb') as output_file:
                    merger.write(output_file)
            PDF_files_to_use.append(file)
        except:
            print "ERROR: For some reason, can't process this PDF: {} . Make sure it's printed out separately.".format(file)
        merger = PdfFileMerger()
    os.remove(TEMP_FILE)

    num_PDFs = len(PDF_files_to_use)
    num_PDFs_per_output_file = int(math.ceil(float(num_PDFs) / split_output_into_this_many_PDF_files))

    print "\nOpening and writing the PDFs...\n"
    merger = PdfFileMerger()
    file_num = 1
    output_file_num = 1
    for file in PDF_files_to_use:
        with open(file, 'rb') as opened_file:
            merger.append(opened_file)
        if file_num % num_PDFs_per_output_file == 0 or file_num == num_PDFs:
            output_file_path = input_folder + "_merged_part_{}.pdf".format(output_file_num)
            print "Writing {} ...".format(output_file_path)
            with open(output_file_path,'wb') as output_file:
                merger.write(output_file)
            output_file_num += 1
            merger = PdfFileMerger() # start anew for next output file
        file_num += 1

    print "Done."

def is_PDF_file(filename):
    parts = filename.split('.')
    if parts[-1].lower() in ["pdf"]:
        return True
    else:
        return False

if __name__ == "__main__":
    run()
