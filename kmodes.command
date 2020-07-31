#!/bin/bash
# Shell installer/launcher for macOS Catalina

set -e # abort on error

DIR="kmodes"

cd ~/Desktop

if [ -d $DIR ]
then
    echo "$DIR already installed."
    cd kmodes
    source kmodes_env/bin/activate
    git clean -fd
    git pull origin master
else
    xcode-select --install || softwareupdate --install -a
    softwareupdate --restart

    git clone https://github.com/mandosoft/kmodes.git
    cd kmodes

    # Install Homebrew for graphviz
    yes | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew update && brew install graphviz

    # Install Python VERSION from source
    curl -O https://www.python.org/ftp/python/3.8.4/python-3.8.4-macosx10.9.pkg
    sudo installer -pkg python-3.8.4-macosx10.9.pkg -target /
    pip3 install --upgrade virtualenv
    virtualenv kmodes_env
    source kmodes_env/bin/activate

    # Install newer Tcl/Tk VERSION from source
    curl -OL https://prdownloads.sourceforge.net/tcl/tk8.6.10-src.tar.gz
    curl -OL https://prdownloads.sourceforge.net/tcl/tcl8.6.10-src.tar.gz
    gunzip < tk8.6.10-src.tar.gz | tar xvf -
    gunzip < tcl8.6.10-src.tar.gz | tar xvf -

    pip install -r requirements.txt
fi

which python
which tcl-tk
python src/qtgui.py

