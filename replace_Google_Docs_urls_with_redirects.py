import requests
from lxml.html import fromstring
import argparse
import re

parser = argparse.ArgumentParser(description='Replace Google-Docs urls with the urls they redirect to.')
parser.add_argument('infile', help='input HTML file')
parser.add_argument('outfile', help='output HTML file')
args = parser.parse_args()

n_urls = 0
with open(args.infile,'rb') as infile:
    with open(args.outfile,'wb') as outfile:
        for line in infile:
            matches = re.findall("href=\"(https?://www\.google\.com/url\?q=[^\"]+)\"", line)
            if matches:
                for url in matches:
                    n_urls += 1
                    print "Original url:\n{}".format(url)
                    resp = requests.get(url)
                    redirected_url = re.search(">([^<]+)</a>", resp.text).group(1)
                    print "Redirected url:\n{}".format(redirected_url)
                    # Get the title of the page too
                    try: # Below lines are from http://stackoverflow.com/a/26812545/1290509
                        redirected_url_resp = requests.get(redirected_url)
                        tree = fromstring(redirected_url_resp.content)
                        title = tree.findtext('.//title').strip()
                        if "403" in title or "404" in title:
                            title = ""
                        else:
                            print "Title:\n{}".format(title)
                    except:
                        title = ""
                    replace_old_url_with_this = redirected_url + """" title="'{}'""".format(title)
                    line = line.replace(url, replace_old_url_with_this.encode('utf-8'))
                    print ""
            outfile.write(line)
    print "Found and replaced {} urls.".format(n_urls)