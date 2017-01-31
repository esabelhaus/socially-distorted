#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

activate="$DIR/twit/bin/activate"

if [ ! -f "$activate" ]
then
    echo "ERROR: activate not found at $activate"
    exit 1
fi

source $activate

python $DIR/fortune.py

deactivate
