#!/usr/bin/env python
import urllib3, sys, argparse, re, datetime, time
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
gen_comment = str(soup.findAll(text=lambda text:isinstance(text, Comment))[1])
gen_dt = re.findall(r"\d+",gen_comment)
repo_dt = datetime.datetime(int(gen_dt[0]),int(gen_dt[1]),int(gen_dt[2]),int(gen_dt[3]),int(gen_dt[4]),int(gen_dt[5]),int(gen_dt[6]))
unixtime = time.mktime(repo_dt.timetuple())
print "Version: \033[1;36m"+str(int(unixtime))+"\033[0m ("+str(repo_dt)+")"

#Get results
script.platforms.get(soup,".")
