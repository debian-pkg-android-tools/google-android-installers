#!/usr/bin/env python
import urllib3, sys, argparse, re
import script.platforms
from bs4 import BeautifulSoup, Comment

#Metadata
progversion = "0.1"
progname="platforms-fetcher"
progdesc="Parser for repository-11.xml to fetch SDK Platforms list"

parser = argparse.ArgumentParser(prog=progname, description=progdesc)
args = parser.parse_args()

url = ""
print "Select a mirror:"
print "[1]: https://dl.google.com"
print "[2]: http://mirrors.neusoft.edu.cn"
print "[3]: http://android-mirror.bugly.qq.com:8080"
while True:
    choice = raw_input("Enter the choice [1/2/3] : ")
    if choice == "1":
        url = "https://dl.google.com/android/repository/repository-11.xml"
	break
    elif choice == "2":
        url = "http://mirrors.neusoft.edu.cn/android/repository/repository-11.xml"
	break
    elif choice == "3":
        url = "http://android-mirror.bugly.qq.com:8080/android/repository/repository-11.xml"
        break
    else:
        print "Wrong choice.."

#Fetch XML File
hdr = {"User-Agent": "Mozilla/5.0"}
print(("Fetching "+url))
http = urllib3.PoolManager()
req = http.request('GET',url,headers=hdr)
if req.status != 200:
   print("HTTP Error: %s" % req.status)
   quit()

soup = BeautifulSoup(req.data, "xml")

#Get results
script.platforms.get(soup,".")
