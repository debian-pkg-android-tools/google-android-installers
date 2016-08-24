def generate(postinst,api_level):
    f = open("script/maintscript/google-android-build-tools-X-installer.postrm.ex")
    i = f.read()
    o = open(postinst, "w")
    o.write(i.replace("$X",api_level))
    o.close()
    print ":... \033[0;34mGENERATED\033[0m google-android-build-tools-"+api_level+"-installer.config"
