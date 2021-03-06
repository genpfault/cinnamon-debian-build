#!/usr/bin/env python

import codecs
import optparse
import os
import subprocess
import sys
import tempfile
import glob

# script location
script_dir = os.path.dirname(os.path.realpath(__file__))

# create output directories
os.chdir(script_dir)
os.system('mkdir -p deb')
os.system('mkdir -p logs')


def build_package(package, options):
    # grab SHA1 of package
    print 'Getting SHA1...'
    os.chdir(script_dir)
    os.chdir(package)
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'])[:7]

    # create & populate temp. directory
    print 'Creating & populating temporary directory...'
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)
    os.system('cp -R {0}/{1} .'.format(script_dir, package))
    package = os.path.basename(package)
    os.chdir(package)

    # discover and install build dependencies
    if options.install_deps:
        print 'Installing build dependencies...'
        os.system('sudo mk-build-deps --tool="apt-get -o Debug::pkgProblemResolver=yes --no-install-recommends -y" --install --remove')

    # build package
    print 'Building package...'
    if options.source:
        os.system('dpkg-buildpackage -S -Zxz -uc -us')
        os.system('cp -v ../*.dsc {0}/deb/'.format(script_dir))
        os.system('cp -v ../*.xz {0}/deb/'.format(script_dir))
        os.system('cp -v ../*.changes {0}/deb/'.format(script_dir))
    else:
        if options.i386:
            os.system('dpkg-buildpackage -B -ai386 -Zxz -uc -tc 2>&1 | tee build.log')
        else:
            os.system('dpkg-buildpackage -b -Zxz -uc -tc 2>&1 | tee build.log')
        os.system('cp -v build.log {0}/logs/{1}.log'.format(script_dir, package))
        os.system('cp -v ../*.deb {0}/deb/'.format(script_dir))
        if options.install:
            # install built package(s)
            os.chdir('..')
            for deb in glob.glob('*.deb'):
                os.system('sudo dpkg --install {0}'.format(deb))
            os.system('sudo apt-get -y -f install')

    # cleanup
    print 'Cleaning up...'
    os.chdir(script_dir)
    os.system('rm -rf {0}'.format(temp_dir))
    print "---------------------------------------------------------------"
    return

# options
parser = optparse.OptionParser()
parser.add_option('-s', '--source', dest='source', action='store_true', help='Build source package')
parser.add_option('-i', '--i386', dest='i386', action='store_true', help='Build i386 binary package')
parser.add_option("-d", "--install-deps", dest="install_deps", action="store_true", help="Install development dependencies")
parser.add_option("-n", "--install", dest="install", action="store_true", help="Install built package")
(options, packages) = parser.parse_args()

if len(packages) == 0:
    # no packages given, build 'em all
    packages = [
        'cinnamon-translations',
        'cinnamon-desktop',
        'cinnamon-menus',
        'cinnamon-session',
        'cinnamon-settings-daemon',
        'python-xapp',
        'cinnamon-screensaver',
        'mozjs38',
        'cjs',
        'cinnamon-control-center',
        'muffin',
        'cinnamon',
        'nemo',
        'nemo-extensions/nemo-python',
        'nemo-extensions/nemo-audio-tab',
        'nemo-extensions/nemo-compare',
        'nemo-extensions/nemo-dropbox',
        'nemo-extensions/nemo-emblems',
        'nemo-extensions/nemo-fileroller',
        'nemo-extensions/nemo-gtkhash',
        'nemo-extensions/nemo-image-converter',
        'nemo-extensions/nemo-media-columns',
        'nemo-extensions/nemo-pastebin',
        'nemo-extensions/nemo-preview',
        'nemo-extensions/nemo-rabbitvcs',
        'nemo-extensions/nemo-repairer',
        'nemo-extensions/nemo-seahorse',
        'nemo-extensions/nemo-share',
        'nemo-extensions/nemo-terminal',
    ]
    options.install_deps = True
    options.install = True

# build given package(s)
for i in range(0, len(packages)):
    package = packages[i]
    if package == '':
        sys.exit(1)
    if package[-1] == '/':
        package = package[:-1]
    if not os.path.exists('{0}/{1}'.format(script_dir, package)):
        print 'E: package \'{0}\' not found'.format(package)
        sys.exit(1)

    build_package(package, options)
