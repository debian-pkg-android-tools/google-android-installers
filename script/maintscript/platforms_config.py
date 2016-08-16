def generate(config,api_level):
    f = open("script/maintscript/google-android-platform-X-installer.config.ex")
    i = f.read()
    o = open(config, "w")
    o.write(i.replace("$X",api_level))
    o.close()
    print ":... \033[0;34mGENERATED\033[0m google-android-platform-"+api_level+"-installer.config"
