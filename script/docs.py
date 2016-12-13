import re, os, glob, shutil, subprocess, sys

def copy_debian_template(pkg_name):
    dst = os.path.join('source-packages', 'google-android-' + pkg_name + '-installer', 'debian')
    po = os.path.join(dst, 'po')
    source = os.path.join(dst, 'source')
    if not os.path.exists(source):
        os.makedirs(source)
    shutil.copy('debian-templates/compat', dst)
    shutil.copy('debian-templates/config', dst)
    shutil.copy('debian-templates/copyright', dst)
    shutil.copy('debian-templates/dirs', dst)
    shutil.copy('debian-templates/gbp.conf', dst)
    shutil.copy('debian-templates/lintian-overrides', dst)
    shutil.copy('debian-templates/postrm', dst)
    shutil.copy('debian-templates/rules', dst)
    shutil.copy('debian-templates/substvars', dst)
    shutil.copy('debian-templates/templates', dst)

    shutil.copy('debian-templates/source/format', source)

    try:
        for f in glob.glob(dst + '/[a-rt-z]*'):
            o = subprocess.check_output(['sed', '-i',
                                         '-e', 's,%PKG_NAME%,' + pkg_name + ',g',
                                         f],
                                    universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit(1)


def get(soup):
    pkg_dir = os.path.join('source-packages', 'google-android-sdk-docs-installer') + '/'
    #Get SDK docs informations
    doc_archive = soup.doc

    archive = doc_archive.archives.archive.url.string
    sha1 = doc_archive.archives.archive.checksum.string

    postinst = pkg_dir+"debian/postinst"
    install = pkg_dir+"debian/install"
    sha1sum = pkg_dir+"for-postinst/"+archive+".sha1"
    rules = pkg_dir+"debian/rules"

    version = doc_archive.find('api-level').string
    revision = re.search("_r[0-9]*",archive).group()[2:]
    print "\033[1;35m- Google Android SDK Docs\033[0m ("+version+")"

    # Generate/Update <package>.install
    if os.path.isfile(install):
        f = open(install)
        current_sha1sum = re.search("docs-.+.zip.sha1",f.readlines()[1]).group()
        if current_sha1sum == archive+".sha1":
            print("\033[0;32mOK\033[0m google-android-sdk-docs-installer.install")
        else:
            print("\033[0;33mOUTDATED\033[0m google-android-sdk-docs-installer.install")
            f.seek(0)
            i = f.read()
            o = open(install,"w")
            o.write(i.replace(current_sha1sum, archive+".sha1"))
            print(":... \033[0;34mUPDATED\033[0m from "+current_sha1sum+" to "+archive)
            o.close()
    else:
         print("\033[0;31mNOT EXIST\033[0m google-android-sdk-docs-installer.install")

    #Generate SHA1
    for f in glob.glob(pkg_dir+"for-postinst/*.sha1"):
        os.remove(f)  # delete old ones
    with open(pkg_dir+"for-postinst/"+archive+".sha1", "w") as fp:
        fp.write(sha1+"  "+archive)
        print ":... \033[0;34mGENERATED\033[0m "+archive+".sha1"

    # Generate/Update <package>.postinst
    if os.path.isfile(postinst):
        f = open(postinst)
        match = re.search("docs-.+.zip",f.readlines()[4]).group()
        if match == archive:
            print("\033[0;32mOK\033[0m google-android-sdk-docs-installer.postinst")
        else:
            print("\033[0;33mOUTDATED\033[0m google-android-sdk-docs-installer.postinst")
            f.seek(0)
            i = f.read()
            o = open(postinst,"w")
            o.write(i.replace(match, archive))
            print(":... \033[0;34mUPDATED\033[0m from "+match+" to "+archive)
            o.close()
    else:
        print("\033[0;31mNOT EXIST\033[0m google-android-sdk-docs-installer.postinst")

    copy_debian_template('sdk-docs')
