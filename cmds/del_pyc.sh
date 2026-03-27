#! /bin/bash

locs=$(find ../../. -type d -name "__pycache__" >&1)
if [[ "$?" -eq "0" ]]; then
    for loc in $locs; do
        pycFiles=$(find "$loc" -name *.pyc)
        for f in $pycFiles; do
            rm $f
        done
    done
fi

exit 0