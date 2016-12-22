import glob, os, shutil, subprocess, sys

from . import *

def copy_debian_template(pkg_name):
    dst = os.path.join('source-packages', 'google-android-' + pkg_name + '-installer', 'debian')

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

    po = os.path.join(dst, 'po')
    if not os.path.exists(po):
        os.makedirs(po)

    shutil.copy('debian-templates/po/cs.po', po)
    shutil.copy('debian-templates/po/de.po', po)
    shutil.copy('debian-templates/po/fr.po', po)
    shutil.copy('debian-templates/po/id.po', po)
    shutil.copy('debian-templates/po/nl.po', po)
    shutil.copy('debian-templates/po/pt.po', po)
    shutil.copy('debian-templates/po/templates.pot', po)
    shutil.copy('debian-templates/po/POTFILES.in', po)

    try:
        for f in glob.glob(dst + '/*'):
            if not os.path.isfile(f):
                continue
            o = subprocess.check_output(['sed', '-i',
                                         '-e', 's,%PKG_NAME%,' + pkg_name + ',g',
                                         f],
                                    universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit(1)
