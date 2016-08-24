import re, os.path, glob

def get(soup,pif):
    pkg_dir = os.path.join(glob.glob(os.path.expanduser(pif))[0], '')
    #Get m2repository informations
    m2repository_archive = soup.extra.archives.archive

    archive = m2repository_archive.url.string
    sha1 = m2repository_archive.checksum.string

    postinst = pkg_dir+"debian/google-android-m2repository-installer.postinst"
    install = pkg_dir+"debian/google-android-m2repository-installer.install"
    sha1sum = pkg_dir+"for-postinst/default/"+archive+".sha1"
    current_sha1sum = ""

    version = re.search(r"\d{2}",archive).group()
    print "\033[1;34m- Android M2 Repository\033[0m ("+version+")"

    # Generate/Update <package>.install
    if os.path.isfile(install):
        f = open(install)
        current_sha1sum = re.search("android_m2repository.+.zip.sha1",f.readlines()[1]).group()
        if current_sha1sum == archive+".sha1":
            print("\033[0;32mOK\033[0m google-android-m2repository-installer.install")
        else:
            print("\033[0;33mOUTDATED\033[0m google-android-m2repository-installer.install")
            f.seek(0)
            i = f.read()
            o = open(install,"w")
            o.write(i.replace(current_sha1sum, archive+".sha1"))
            print(":... \033[0;34mUPDATED\033[0m from "+current_sha1sum+" to "+archive)
            o.close()
    else:
         print("\033[0;31mNOT EXIST\033[0m google-android-m2repository-installer.install")

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
        match = re.search("android_m2repository.+.zip",f.readlines()[7]).group()
        if match == archive:
            print("\033[0;32mOK\033[0m google-android-m2repository-installer.postinst")
        else:
            print("\033[0;33mOUTDATED\033[0m google-android-m2repository-installer.postinst")
            f.seek(0)
            i = f.read()
            o = open(postinst,"w")
            o.write(i.replace(match, archive))
            print(":... \033[0;34mUPDATED\033[0m from "+match+" to "+archive)
            o.close()
    else:
        print("\033[0;31mNOT EXIST\033[0m google-android-m2repository-installer.postinst")    

