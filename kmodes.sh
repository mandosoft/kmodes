#!/bin/bash
# Shell installer/launcher for macOS Catalina

set -e # abort on error

DIR="kmodes"

cd ~/Desktop

if [ -d $DIR ]
then
    echo "{$DIR} exists."
else
    xcode-select --install || softwareupdate --install -a && softwareupdate --restart
    GIT=git

    yes | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew install python
    brew update && brew upgrade python
    brew install graphviz

    echo "Checking git"
    if [ ! -f $GIT ]; then
        echo "### Git installation failed"
        exit 255
    fi

    $GIT clone https://github.com/mandosoft/kmodes.git
    cd kmodes
    pip3 install -r requirements.txt
fi

git clean -fd
git pull origin master

python3 main.py

