import re

def generate(rules,api_level,revision):
    f = open(rules,"r")
    i = f.read()
    f.seek(0)
    il = f.readlines()
    f.close()
    match = re.search("PLATFORM_"+api_level+"_VERSION = \d+\+r\d+",i)
    if (match):
        if match.group() == "PLATFORM_"+api_level+"_VERSION = "+api_level+"+r"+revision:
            print "\033[0;32mOK\033[0m google-android-platform-"+api_level+"-installer in d/rules"
        else:
            f = open(rules)
            i = f.read()
            o = open(rules, "w")
            i = i.replace(match.group(),"PLATFORM_"+api_level+"_VERSION = "+api_level+"+r"+revision)
            o.write(i)
            o.close()
            print ":... \033[0;34mUPDATED\033[0m google-android-platform-"+api_level+"-installer to revision "+revision
    else:
        print("\033[0;31mNOT EXIST\033[0m google-android-platform-"+api_level+"-installer in d/rules")
        il.insert(1,"\nPLATFORM_"+api_level+"_VERSION = "+api_level+"+r"+revision)
        il.insert(len(il),"\tdh_gencontrol -pgoogle-android-platform-"+api_level+"-installer -- -v$(PLATFORM_"+api_level+"_VERSION) -Tdebian/substvars\n")
        w = open(rules, "w")
        il = "".join(il)
        w.write(il)
        w.close()
        print ":... \033[0;34mGENERATED\033[0m added to d/rules"

