def generate(install,api_level,archive):
    f = open("maintscript/google-android-platform-X-installer.install.ex")
    i = f.read()
    o = open(install, "w")
    i = i.replace("$X",api_level).replace("$Y",archive)
    o.write(i)
    o.close()
    print ":... \033[0;34mGENERATED\033[0m google-android-platform-"+api_level+"-installer.install"
