#!/usr/bin/env python
import urllib3, sys, argparse, re, datetime, time, subprocess
import script.platforms, script.ndk, script.docs, script.m2repository, script.buildtools
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
    choice = raw_input("Enter the choice [1/2/3] (default: 1) : ")
    if choice == "1" or choice == "":
        repo_url = "https://dl.google.com/android/repository/repository-12.xml"
        addon_url = "https://dl.google.com/android/repository/addon.xml"
	break
    elif choice == "2":
        repo_url = "http://mirrors.neusoft.edu.cn/android/repository/repository-12.xml"
        addon_url = "http://mirrors.neusoft.edu.cn/android/repository/addon.xml"
	break
    elif choice == "3":
        repo_url = "http://android-mirror.bugly.qq.com:8080/android/repository/repository-12.xml"
        addon_url = "http://android-mirror.bugly.qq.com:8080/android/repository/addon.xml"
        break
    else:
        print "Wrong choice.."

hdr = {"User-Agent": "Mozilla/5.0"}
http = urllib3.PoolManager()

#Fetch Repository-11 XML File
print(("Fetching "+repo_url))
req = http.request('GET',repo_url,headers=hdr)
if req.status != 200:
   print("HTTP Error: %s" % req.status)
   quit()
repo = BeautifulSoup(req.data, "xml")

#Fetch Addon XML File
print(("Fetching "+addon_url))
req = http.request('GET',addon_url,headers=hdr)
if req.status != 200:
   print("HTTP Error: %s" % req.status)
   quit()
addon = BeautifulSoup(req.data, "xml")

#Get Repository-11 Version
gen_comment = str(repo.findAll(text=lambda text:isinstance(text, Comment))[1])
gen_dt = re.findall(r"\d+",gen_comment)
repo_dt = datetime.datetime(int(gen_dt[0]),int(gen_dt[1]),int(gen_dt[2]),int(gen_dt[3]),int(gen_dt[4]),int(gen_dt[5]),int(gen_dt[6]))
repo_live_version = str(int(time.mktime(repo_dt.timetuple())))
print "* Repository Version: \033[2;36m"+repo_live_version+"\033[0m ("+str(repo_dt)+")"

#Get Addon Version
gen_comment = str(addon.findAll(text=lambda text:isinstance(text, Comment))[0])
gen_dt = re.findall(r"\d+",gen_comment)
repo_dt = datetime.datetime(int(gen_dt[0]),int(gen_dt[1]),int(gen_dt[2]),int(gen_dt[3]),int(gen_dt[4]),int(gen_dt[5]),int(gen_dt[6]))
addon_live_version = str(int(time.mktime(repo_dt.timetuple())))
print "* Addon Version: \033[2;96m"+addon_live_version+"\033[0m ("+str(repo_dt)+")"

max_live = 0
if int(repo_live_version) > int(addon_live_version):
    max_live = int(repo_live_version)
else:
    max_live = int(addon_live_version)

o = open('debian/changelog')
current_version = re.search(r"\d+",o.readline()).group()

if int(current_version) == max_live:
	print "* Package Version: \033[2;32m"+current_version+"\033[0m"
else:
	print "* Package Version: \033[0;31m"+current_version+"\033[0m (Version update to \033[1;4m"+str(max_live)+"\033[0m is suggested)"

#Get results
script.platforms.get(repo,".")
script.ndk.get(repo,".")
script.docs.get(repo,".")
script.m2repository.get(addon,".")
script.buildtools.get(repo,".")

#Removing .pyc files
subprocess.call(["pyclean", "."])
