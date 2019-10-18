#!/usr/bin/env python3
'''
url = https://www.congress.gov/congressional-record
url = https://www.congress.gov/congressional-record/2019/9/24/daily-digest
key = "COMMITTEE MEETINGS FOR"
key = "Taiwan"
'''
import sys
import urllib.request
from html.parser import HTMLParser
import json
from bs4 import BeautifulSoup
import re

def main(argv):
    url = argv[1]
    key = argv[2]
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,} 
    request = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(request) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        mydivs = soup.find("div", {"class": "main-wrapper"})
        with open("main-wrapper.html", "w+") as f:
            f.write(str(mydivs))
        # mystrongs = [td.find("strong") for td in mydivs.findAll("center", text = re.compile('COMMITTEE MEETINGS FOR'))]
        res = mydivs.findAll(text=re.compile(key, re.I))
        if res:
            mystrongs = mydivs.find("center", text = re.compile('COMMITTEE MEETINGS FOR'))
            mystrongs2 = mystrongs.find_next("center")
            print(mystrongs, '\n',mystrongs2)
            print(res)

if __name__ == '__main__':
    main(sys.argv)