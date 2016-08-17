import re, os.path, glob
import maintscript.platforms_install, maintscript.platforms_postinst, maintscript.platforms_postrm, maintscript.platforms_config, maintscript.platforms_templates, maintscript.platforms_dirs, maintscript.platforms_control, maintscript.platforms_lintianoverrides

def get(soup,pif):
    pkg_dir = os.path.join(glob.glob(os.path.expanduser(pif))[0], '')
    # Get platforms list
    platforms_list = soup.findAll('platform') 
    # Show results
    for platform in platforms_list:
        print(("\033[1;33m- "+platform.description.string+"\033[0m"))
        api_level = platform.find('api-level').string
        version =  platform.version.string
        archive = platform.archives.archive.url.string
        revision = re.search("_r[0-9]*",archive).group()[2:]
        sha1 =  platform.archives.archive.checksum.string
        binary = "google-android-platform-"+api_level+"-installer"
        install = pkg_dir+"debian/"+binary+".install"
        postinst = pkg_dir+"debian/"+binary+".postinst"
        postrm = pkg_dir+"debian/"+binary+".postrm"
        config = pkg_dir+"debian/"+binary+".config"
        templates = pkg_dir+"debian/"+binary+".templates"
        dirs = pkg_dir+"debian/"+binary+".dirs"
        overrides = pkg_dir+"debian/"+binary+".lintian-overrides"
        control = pkg_dir+"debian/control"
        sha1sum = pkg_dir+"for-postinst/default/"+archive+".sha1"
        current_sha1sum = ""

        # Generate/Update <package>.install
        if os.path.isfile(install):
            f = open(install)
            current_sha1sum = re.search("(android|platform)-[0-9]*((.[0-9]*)*)?_r[0-9]*(-linux)?.zip.sha1",f.readlines()[1]).group()
            if current_sha1sum == archive+".sha1":
                print("\033[0;32mOK\033[0m "+binary+".install")
            else:
                print("\033[0;33mOUTDATED\033[0m "+binary+".install")
                f.seek(0)
                i = f.read()
                o = open(install,"w")
                o.write(i.replace(current_sha1sum, archive+".sha1"))
                print(":... \033[0;34mUPDATED\033[0m from "+current_sha1sum+" to "+archive+".sha1")
                o.close()
        else:
            print("\033[0;31mNOT EXIST\033[0m "+binary+".install")
            maintscript.platforms_install.generate(install,api_level,archive)       

        # Generate/Update <archive>.sha1
	current_sha1sum_file = pkg_dir+"for-postinst/default/"+current_sha1sum
        generate_sha1 = False
        if current_sha1sum != "":
            if os.path.isfile(current_sha1sum_file):
                f = open(current_sha1sum_file)
                current_sha1 = re.search(r'\b[0-9a-f]{5,40}\b',f.readlines()[0]).group()
                if current_sha1sum_file != sha1sum:
                    # Remove outdated sha1 file
                    try:
		        os.remove(current_sha1sum_file)
	            except OSError:
		        pass
                    # Generate new sha1 file
                    if os.path.isfile(sha1sum):
                        print("\033[0;32mOK\033[0m "+archive+".sha1")
                    else:
                        generate_sha1 = True
                elif current_sha1 != sha1:
                    generate_sha1 = True
        else:
            generate_sha1 = True

        #Generate SHA1 if needed
        if generate_sha1 == True:
            i = open(pkg_dir+"for-postinst/default/"+archive+".sha1", "w+")
            i.write(sha1+"  "+archive)
            i.close()
            print ":... \033[0;34mGENERATED\033[0m "+archive+".sha1"

        # Generate/Update <package>.postinst
        if os.path.isfile(postinst):
            f = open(postinst)
            match = re.search("r[0-9]+",f.readlines()[7]).group()[1:]
            if int(match) == int(revision):
                print("\033[0;32mOK\033[0m "+binary+".postinst")
            else:
                print("\033[0;33mOUTDATED\033[0m "+binary+".postinst")
                f.seek(0)
                i = f.read()
                o = open(postinst,"w")
                o.write(i.replace(match, revision))
                print(":... \033[0;34mUPDATED\033[0m from revision "+match+" to "+revision)
                o.close()
        else:
            print("\033[0;31mNOT EXIST\033[0m "+binary+".postinst")
            maintscript.platforms_postinst.generate(postinst,api_level,archive)

        #Generate <package>.postrm
        if os.path.isfile(postrm):
           print("\033[0;32mOK\033[0m "+binary+".postrm")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".postrm")
           maintscript.platforms_postrm.generate(postrm,api_level)

        #Generate <package>.config
        if os.path.isfile(config):
           print("\033[0;32mOK\033[0m "+binary+".config")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".config")
           maintscript.platforms_config.generate(config,api_level)

        #Generate <package>.templates
        if os.path.isfile(templates):
           print("\033[0;32mOK\033[0m "+binary+".templates")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".templates")
           maintscript.platforms_templates.generate(templates,api_level)

        #Generate <package>.dirs
        if os.path.isfile(dirs):
           print("\033[0;32mOK\033[0m "+binary+".dirs")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".dirs")
           maintscript.platforms_dirs.generate(dirs,api_level)

        #Generate <package>.lintian-overrides
        if os.path.isfile(overrides):
           print("\033[0;32mOK\033[0m "+binary+".lintian-overrides")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+".lintian-overrides")
           maintscript.platforms_lintianoverrides.generate(overrides,api_level)

        #Add package to d/control
        if "platform-"+api_level+"-" in open(control).read():
           print("\033[0;32mOK\033[0m "+binary+" in d/control")
        else:
           print("\033[0;31mNOT EXIST\033[0m "+binary+" in d/control")
           maintscript.platforms_control.generate(control,api_level,archive)
