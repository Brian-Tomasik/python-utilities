"""
By Brian Tomasik.
First version: 24 Mar. 2018; last update: 24 Mar. 2018.
This program is written for Python 2.

This program allows you to track changes to a specified set of web pages over time. This can be useful, for example, to see what edits your colleagues are making to a shared website, or to review the edits that you've made to your own site to make sure you didn't accidentally mess something up. Online services providing this functionality are often surprisingly expensive, so I created my own program instead.

You run this program as follows. Put it in some empty directory. Add to that directory a `urls_to_check.txt` file containing the urls you want to track for changes, one url per line. These can be from any website and can be any file type (.html, .pdf, .jpg, etc). Run `python check_website_updates.py` once to download the urls for the first time. This could take a while if you have a lot of urls, because I delay for some number of seconds between each download. Then, whenever you want to do a diff of all the pages, just rerun the program: `python check_website_updates.py`. Each time you want to do another diff (against your most recent download), rerun the program once more. So, for example, if you want to do a diff every week, just run `python check_website_updates.py` once a week and see the latest changes to your tracked websites.

This program calls `diff -r` to diff the two directories of downloaded files. HTML files ordinarily contain a whole paragraph of text on one line. It can be annoying to look at a diff of a whole paragraph against another, especially if only one or two words has changed somewhere within that paragraph. To make inspection of the diff output easier, I added newlines after each declarative sentence within the downloaded .html and other text files, so that if you only edited one sentence, only that one sentence will appear in the diff output, not the whole paragraph.

I also remove some lines from HTML files that are dynamically generated in WordPress, since these will differ on successive downloads of a page even if the page's core content hasn't changed.

Note: When I say this program downloads urls, I mean it downloads individual files, like `http://www.mywebsite.com/planets/index.html` or `https://www.anothersite.net/stars.pdf`. It doesn't find all the urls on a domain. If you want to do that, you have to generate the list of all the urls on a domain yourself. (Sorry!)
"""

import os
import re
import urllib
import time
import shutil
import subprocess
from datetime import datetime

NAME_OF_OLD_DIR = 'old'
NAME_OF_NEW_DIR = 'new'
STARTING_SECONDS_BETWEEN_DOWNLOADS = 1
MAX_SECONDS_BETWEEN_DOWNLOADS = 30

def run():
    urls_to_check = get_urls_list("urls_to_check.txt")
    if len(urls_to_check) < 1:
        print "You have no urls to check."
        return
    if os.path.isdir(NAME_OF_OLD_DIR):
        print "Note: This program will delete the '{}' directory. Are you sure you want to continue? Enter 'y' if yes. Enter anything else to abort.".format(NAME_OF_OLD_DIR)
        answer = raw_input()
        if answer is not 'y':
            return
        shutil.rmtree(NAME_OF_OLD_DIR)
        print "Removed the past '{}' directory, since it's no longer needed.".format(NAME_OF_OLD_DIR)
    if os.path.isdir(NAME_OF_NEW_DIR):
        os.rename(NAME_OF_NEW_DIR, NAME_OF_OLD_DIR)
        print "Renamed the past '{}' directory to '{}', since it's now the old directory to be compared against a newly downloaded set of web pages.".format(NAME_OF_NEW_DIR, NAME_OF_OLD_DIR)
    os.mkdir(NAME_OF_NEW_DIR)
    download_urls_to_check(urls_to_check, NAME_OF_NEW_DIR)
    if os.path.isdir(NAME_OF_OLD_DIR):
        print "Now running `diff -r {} {}`:".format(NAME_OF_OLD_DIR, NAME_OF_NEW_DIR)
        subprocess.call(['diff', '-r', NAME_OF_OLD_DIR, NAME_OF_NEW_DIR])
    else:
        print "There's no old version of the files to compare against. Rerun this program later in order to do a diff against what you just downloaded."

def get_urls_list(urls_list_filename):
    urls_to_check = []
    with open(urls_list_filename,"r") as urls_list_file:
        for line in urls_list_file:
            line = line.strip()
            if line.startswith("http"):
                urls_to_check.append(line)
            else:
                print "Warning: This url doesn't start with the letters 'http': {}".format(line)
    return urls_to_check

def download_urls_to_check(urls_to_check, destination_dir):
    seconds_between_downloads = STARTING_SECONDS_BETWEEN_DOWNLOADS
    urllib.URLopener.version = 'Firefox/2.0.0.11' # Some sites block downloads without a User-Agent like this.
    for url in urls_to_check:
        filename_for_this_web_page = create_filename_from_url(url)
        destination_filename_including_path = os.path.join(destination_dir, filename_for_this_web_page)
        urllib.urlretrieve(url, destination_filename_including_path)
        if url_is_probably_a_text_file(url):
            make_each_sentence_its_own_line_in_file_and_remove_dynamic_WordPress_stuff(destination_filename_including_path)
        print "Downloaded {} . Sleeping {} seconds.".format(url, seconds_between_downloads)
        time.sleep(seconds_between_downloads)
        if seconds_between_downloads < MAX_SECONDS_BETWEEN_DOWNLOADS:
            """I want to start out downloading fast and get slower over time so that if you only have a small number of urls, this program is fast, but if you have lots of urls, you don't hit the server too rapidly for too many urls."""
            seconds_between_downloads = seconds_between_downloads + 1
    write_timestamp_file(destination_dir)

def url_is_probably_a_text_file(url):
    """Try to guess if the url points to a file that can be read as plain text (.txt, .html, etc) or to a binary file (.pdf, .jpg, etc)."""
    if url.endswith("/"): # This is short for `/index.html`.
        return True
    some_text_file_formats = [".html", ".htm", ".txt", ".tex", ".xml"]
    for format in some_text_file_formats:
        if url.endswith(format):
            return True
    return False

def make_each_sentence_its_own_line_in_file_and_remove_dynamic_WordPress_stuff(destination_filename_including_path):
    """This step processes downloaded text and HTML files to make them nicer to diff. One way is to make the files have more lines that are each shorter. This makes it easier to see the relevant changes in a diff. Without this, the diff might return a big paragraph, and you'd have to look through the whole paragraph to find the change. I also remove WordPress lines that typically change from one download to the next."""
    with open(destination_filename_including_path,"r") as read_from_this_file:
        with open(destination_filename_including_path + ".txt","w") as write_to_this_file:
            for line in read_from_this_file:
                if line_includes_dynamic_WordPress_stuff(line):
                    continue
                split_line = line.split(". ") # split on end of sentences
                for part in split_line:
                    if not part.endswith("\n"):
                        part = part + ".\n"
                    write_to_this_file.write(part)
    os.remove(destination_filename_including_path)

def line_includes_dynamic_WordPress_stuff(line):
    text_that_if_present_suggests_a_dynamic_line = ["article:modified_time", "og:updated_time", "entry-date published", "Dynamic page generated in", "Cached page generated by WP-Super-Cache on", 'class="widget widget_text"><h4>Contact</h4>']
    for text in text_that_if_present_suggests_a_dynamic_line:
        if text in line:
            return True
    if "Served from: " in line and " by W3 Total Cache" in line:
        return True
    return False

def create_filename_from_url(url):
    """Create a simplified file name without special url characters to which to save the HTML, PDF, or other file."""
    url_before_extension_if_any, extension_if_any = os.path.splitext(url)
    return re.sub('[^\w]', '', url_before_extension_if_any) + extension_if_any

def write_timestamp_file(dir):
    timestamp_file_path = os.path.join(dir, "timestamp_for_this_download.txt")
    with open(timestamp_file_path,"w") as timestamp_file:
        timestamp = datetime.now().strftime('%Y %b %d %H:%M:%S')
        timestamp_file.write("This download was completed: {}.\n".format(timestamp))

if __name__ == "__main__":
	run()
