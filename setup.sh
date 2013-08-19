#!/usr/bin/env bash
# Lyle Scott, III  // lyle@digitalfoo.net // Copyright 2013

if [ ! $(type -P virtualenv) ]; then
    echo "virtualenv needs to be installed or install the following python "
    echo "libs manually and skip setup.sh:"
    cat venv/requirements.txt
    exit 1
fi

echo -e "\n#\n# Updating geo dat files...\n#\n"
./dats/update.sh

echo -e "\n#\n# Updating markerclustererplus js files...\n#\n"
./html/update.sh

echo -e "\n#\n# Installing virtual environment...\n#\n"
virtualenv --no-site-packages venv

echo -e "\n#\n# Switching to virtual environment...\n#\n"
source venv/bin/activate

echo -e "\n#\n# Installing needed python libraries in virtual environment...\n#\n"
pip install -r venv/requirements.txt
