"""
By Brian Tomasik
First written: 11 Aug. 2017; last update: 3 Sep. 2017

This program is part of my process of backing up important websites on paper. After downloading a WordPress website
using SiteSucker, I want to extract just the interesting HTML content from each web page, ignoring the boilerplate
content that WordPress includes before and after the main body of the HTML page. That's what this program does. It
runs through a downloaded website folder, finds each HTML file, and sucks out the interesting HTML content from each
file. The sucked-out contents are combined into a single output file. That output file can then be imported into a
Word/etc. document and converted to PDF for printing out on paper.

Sample usage: To extract and combine the HTML files in mywebsitedirectory/ , run:
  python extract_valuable_HTML_from_WordPress_site_download.py mywebsitedirectory
"""

import sys
import os

def run(also_include_txt_files=True):
    input_folder = sys.argv[1]  # input WordPress site-download folder (without any ending "/"); has to be in same folder as the .py program
    all_HTML_files = []

    print "Getting a list of all HTML files...\n"
    for (path, dirs, files) in os.walk(input_folder):
        for file in files:
            if is_HTML_file_and_not_a_redundant_blog_comments_file(file, also_include_txt_files):
                all_HTML_files.append(os.path.join(path, file))

    output_file_path = input_folder + "_extracted.html"
    print "Extracting and writing the core HTML from the files to {} ...\n".format(output_file_path)
    with open(output_file_path, 'w') as output_file:
        output_file.write("Extracted HTML from the website {} :\n\n\n".format(input_folder))
        for file in all_HTML_files:
            output_file.write(extract_HTML(file) + "\n\n\n")

    print "\nDone."

def is_HTML_file_and_not_a_redundant_blog_comments_file(filename, also_include_txt_files):
    if also_include_txt_files:
        if get_file_extension(filename) == "txt":
            return True
    if get_file_extension(filename) in ["html", "htm"] and "replytocom" not in filename:
        return True
    else:
        return False

def get_file_extension(filename):
    parts = filename.split('.')
    return parts[-1].lower()

def extract_HTML(HTML_file_path):
    with open(HTML_file_path) as input_HTML_file:
        if get_file_extension(HTML_file_path) == "txt":
            extracted_lines = input_HTML_file.readlines()
            if "survey_source" in HTML_file_path: # see if this is the file 'survey_source.txt'
                del extracted_lines[1] # avoid a stylesheet file that, if included, would mess with formatting of the output of this program
        else:
            include_lines_now = False
            extracted_lines = []
            for line in input_HTML_file:
                if not include_lines_now and "<h1" in line:  # This heuristic works for all websites I care about.
                    include_lines_now = True
                if include_lines_now and "<footer" in line:  # This heuristic works for all websites I care about.
                    include_lines_now = False
                    break
                if include_lines_now:
                    extracted_lines.append(line)
        if len(extracted_lines) == 0:
            print "WARNING: File {} had no extracted content".format(HTML_file_path)
        return "".join(line for line in extracted_lines) # Based on https://waymoot.org/home/python_string/

if __name__ == "__main__":
    run()
