#! /bin/bash

# This is untested so be careful when running it

echo "Are you sure you want to reset the database?"
read confirmation
if [[ $confirmation == "y" ]]; then
    ./del_pyc.sh
    filelocs=$(find ../. -type f -name "db.sqlite3" >&1)
    if [[ "$?" -eq "0" ]]; then
        for loc in $filelocs; do
            rm "$loc"
        done
    else
        echo "Could not find db"
    fi
fi
exit 0