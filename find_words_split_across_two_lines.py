"""
By Brian Tomasik
20 Aug. 2017

This program solves a deficiency in (simplistic uses of) grep: namely, that
unless you do fancy regular expressions, grep doesn't find search terms that
are split across two lines. For example, suppose you're looking for the word
"password" in files, but that word might be split across two lines, possibly
with some junk characters thrown in, like this:

the boy took his pa =
ssword into the kitchen

The current program allows for "grepping" these two lines. The program searches
recursively all files in the directory from which it's run. You can search for
multiple terms by comma-separating them as input arguments. For example, you
might run:

python find_words_split_across_two_lines.py "username,password,ssn number"

This program only searches for terms split across lines, so it won't find
terms in the middle of lines. For that you should still use grep as a complement
to this program. Following is the grep command I use:

grep -rioEn ".{0,20}mysearchstring.{0,20}" .
"""

import sys
import os

def run(allow_whole_word_on_one_line=True, num_junk_chars_allowed_between_word_parts_per_line=3):
    comma_separated_strings_to_search_for = sys.argv[1].lower()  # example: "username,password,social security number"
    strings_to_search_for = comma_separated_strings_to_search_for.split(',')

    for (path, dirs, files) in os.walk('.'):
        for file in files:
            search_file(os.path.join(path, file), strings_to_search_for, allow_whole_word_on_one_line,
                        num_junk_chars_allowed_between_word_parts_per_line)

def search_file(file_path, strings_to_search_for, allow_whole_word_on_one_line,
                num_junk_chars_allowed_between_word_parts_per_line):
    with open(file_path, 'rb') as input_file:
        prev_line = ""
        for line in input_file:
            line = line.lower().strip("\n\r")
            for string in strings_to_search_for:
                if found_string(string, line, prev_line, allow_whole_word_on_one_line,
                                num_junk_chars_allowed_between_word_parts_per_line):
                    print "\nIn file {} found string '{}' :\n{}\n{}\n".format(file_path, string, prev_line, line)
            prev_line = line

def found_string(string, second_line, first_line, allow_whole_word_on_one_line,
                 num_junk_chars_allowed_between_word_parts_per_line):
    for i in range(len(string)+1):
        first_part = string[:i]
        second_part = string[i:]
        if not allow_whole_word_on_one_line:
            if first_part == "" or second_part == "":
                continue
        num_chars_to_use_at_end_of_first_line = len(first_part) + num_junk_chars_allowed_between_word_parts_per_line
        num_chars_to_use_at_beginning_of_second_line = len(second_part) + \
                                                       num_junk_chars_allowed_between_word_parts_per_line
        ending_part_of_first_line = first_line[-num_chars_to_use_at_end_of_first_line:]
        beginning_part_of_second_line = second_line[:num_chars_to_use_at_beginning_of_second_line]
        if first_part in ending_part_of_first_line and second_part in beginning_part_of_second_line:
                return True
    return False

if __name__ == "__main__":
    run()
