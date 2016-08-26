import re

def generate(rules,api_level,version):
    f = open(rules,"r")
    i = f.read()
    f.seek(0)
    il = f.readlines()
    f.close()
    match = re.search("BUILD_TOOLS_"+api_level+"_VERSION = \d+.\d+.\d+",i)
    if (match):
        if match.group() == "BUILD_TOOLS_"+api_level+"_VERSION = "+version:
            print "\033[0;32mOK\033[0m google-android-build-tools-"+api_level+"-installer in d/rules"
        else:
            f = open(rules)
            i = f.read()
            o = open(rules, "w")
            i = i.replace(match.group(),"BUILD_TOOLS_"+api_level+"_VERSION = "+version)
            o.write(i)
            o.close()
            print ":... \033[0;34mUPDATED\033[0m google-android-build-tools-"+api_level+"-installer to version "+version
    else:
        print("\033[0;31mNOT EXIST\033[0m google-android-build-tools-"+api_level+"-installer in d/rules")
        il.insert(1,"\nBUILD_TOOLS_"+api_level+"_VERSION = "+version)
        il.insert(len(il),"\tdh_gencontrol -pgoogle-android-build-tools-"+api_level+"-installer -- -v$(BUILD_TOOLS_"+api_level+"_VERSION) -Tdebian/substvars\n")
        w = open(rules, "w")
        il = "".join(il)
        w.write(il)
        w.close()
        print ":... \033[0;34mGENERATED\033[0m added to d/rules"

