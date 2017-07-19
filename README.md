`build-packages.py` is a Python script to automate building Debian packages for the Cinnamon desktop environment in the proper order.

The Cinnamon project submodules are pinned to the latest stable release for convenience.

I recommend spinning up a clean Debian Strech VM to build the packages in, `mk-build-deps` pulls in a bunch of packages you may or may not want cluttering up your day-to-day system.  2-4 cores, 2-4 GiB of memory, and ~10 GiB worth of disk should be enough.  Uncheck everything but `standard system utilities` in `tasksel`.

Build procedure:

    sudo apt-get install git-core devscripts dpkg-dev
    git clone https://github.com/genpfault/cinnamon-debian-build.git
    cd cinnamon-debian-build
    git submodule update --init --recursive
    ./build-packages.py

Packages are copied to `cinnamon-debian-build/deb`.

Building everything takes around 20 minutes on a Xeon D-1521 in a 4-core, 4 GiB KVM VM.

You'll also want to install the `xorg` metapackage as well as the display manager (LightDM, GDM, KDM, etc.) of your choice.

