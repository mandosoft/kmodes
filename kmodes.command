#!/bin/bash
# Shell installer/launcher for macOS Catalina

set -e # abort on error

DIR="kmodes"

cd ~/Desktop

if [ -d $DIR ]
then
    echo "{$DIR} exists."
    cd kmodes
else
    xcode-select --install || softwareupdate --install -a && softwareupdate --restart

    # Install Homebrew
    yes | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

    # TODO: Install ActiveTcl version
    cd kmodes
    sudo installer -pkg lib/ActiveTcl-8.6.9.8609.2-macosx10.9-x86_64-93b04018.pkg -target /
    
    # Install Python from source
    curl -O https://www.python.org/ftp/python/3.8.4/python-3.8.4-macosx10.9.pkg
    sudo installer -pkg python-3.8.4-macosx10.9.pkg -target /

    brew update && brew install graphviz
    brew uninstall python3

    git clone https://github.com/mandosoft/kmodes.git
    cd kmodes
    pip3 install -r requirements.txt
fi

git clean -fd
git pull origin master

python3 main.py

