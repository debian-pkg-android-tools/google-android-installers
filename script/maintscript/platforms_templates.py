from shutil import copyfile

def generate(templates,api_level):
    copyfile("script/maintscript/google-android-platform-X-installer.templates.ex", templates)
    print ":... \033[0;34mGENERATED\033[0m google-android-platform-"+api_level+"-installer.templates"
