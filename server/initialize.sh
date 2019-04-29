#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Please supply name of virtualenv"
    echo "USAGE virtualenvName [virtualEnvLocation]"
    exit 1
elif [[ $# -eq 2 ]]; then
    WORKON_HOME="$2"
elif [[ $# -gt 2 ]]; then
    echo "Too many arguments"
fi

INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

if [[ $INVENV -eq 1 ]]; then
    echo "In virtual environment...skipping creation of venv"
else
    echo "creating virtual environment"
    if [[ $WORKON_HOME ]]; then
        mkdir -p "$WORKON_HOME"
        cd "$WORKON_HOME"
    fi
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv --python=/usr/bin/python $1
fi

cd "$WORKON_HOME/$1"
./bin/pip install mysql-connector-python django mysqlclient
./bin/pip install mysql-connector-python django mysqlclient python-dateutil django-material python-magic uwsgi
echo "export DJANGO_SETTINGS_MODULE=dashboard.settings" >> ./bin/activate.fish
echo ""
echo "Please cd into $WORKON_HOME/$1 and run . bin/activate.fish"
