#!/bin/bash
#set -x
set -e
set -u


if [ $# -ne 1 ] ; then
    >&2 echo "error! URL param is missing!"
    >&2 echo "example usage:"
    >&2 echo "$0 \"0.0.0.0:8000\""
    exit 1
fi

CWD=$(pwd)
URL=${1}

echo "CWD=${CWD}"
python2 manage.py runserver --insecure -v3 ${URL}

