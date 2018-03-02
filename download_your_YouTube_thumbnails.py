"""
By Brian Tomasik
2 Mar. 2018

This program downloads the (highest-resolution) thumbnails of your YouTube videos based on the .json metadata for those videos. First, use Google Takeout to export your YouTube data. It should have a folder that contains, among other files, the .json metadata files for your videos. Then put this script in that folder and run this script. It will download the thumbnails for your videos into the same folder.
"""

import os
import unicodedata
import re
import json
import urllib
import time

def run():
	for item in os.listdir(u'.'):
		if os.path.isfile(item) and not item.startswith('.') and item.endswith('.json'):
			download_thumbnail(item)
	print "Done."

def download_thumbnail(json_filename):
	with open(json_filename) as json_file:
		data = json.load(json_file)
		thumbnail_url = data[0]['snippet']['thumbnails']['high']['url']
		image_path, image_extension = os.path.splitext(thumbnail_url)
		video_title = data[0]['snippet']['title']
		destination_image_filename = normalize_title_to_get_filename(video_title) + image_extension
		urllib.urlretrieve(thumbnail_url, destination_image_filename)
		print "Downloaded {}. Sleeping 5 seconds.".format(destination_image_filename)
		time.sleep(5)

def normalize_title_to_get_filename(video_title):
	"""Much of this code is taken from https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename"""
	filename = unicodedata.normalize('NFKD',video_title).encode('ascii', 'ignore')
	filename = re.sub('[^\w\s-]', '', filename)
	filename = re.sub('[-\s]+', '_', filename)
	return filename

if __name__ == "__main__":
	run()
