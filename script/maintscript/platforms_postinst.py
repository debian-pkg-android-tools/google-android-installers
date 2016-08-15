def generate(postinst,api_level,archive):
    f = open("maintscript/google-android-platform-X-installer.postinst.ex")
    i = f.read()
    o = open(postinst, "w")
    i = i.replace("$X",api_level).replace("$Y",archive)
    o.write(i)
    o.close()
    print ":... \033[0;34mGENERATED\033[0m google-android-platform-"+api_level+"-installer.postinst"
