from shutil import copyfile

def generate(templates,api_level):
    copyfile("script/maintscript/google-android-build-tools-X-installer.templates.ex", templates)
    print ":... \033[0;34mGENERATED\033[0m google-build-tools-"+api_level+"-installer.templates"
