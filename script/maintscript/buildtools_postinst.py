def generate(postinst,api_level,archive,version):
    f = open("script/maintscript/google-android-build-tools-X-installer.postinst.ex")
    i = f.read()
    o = open(postinst, "w")
    i = i.replace("$X",api_level).replace("$Y",archive).replace("$Z",version)
    o.write(i)
    o.close()
    print ":... \033[0;34mGENERATED\033[0m google-android-build-tools-"+api_level+"-installer.postinst"
