#!/bin/bash

set -e # abort on error
# To my loving spacewitch
# shellcheck disable=SC2164
cd src/kmodes_alpha
echo "compiling kmodes to executable"
pyinstaller --onefile \
--name kmodes_app \
--specpath ../../ \
-p kmodes_alpha \
--windowed \
--console \
main.py

cd dist
./kmodes_app