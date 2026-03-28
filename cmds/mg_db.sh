#! /bin/bash

python ../manage.py makemigrations mybase
if [[ "$?" -eq "0" ]]; then
    python ../manage.py migrate
fi

exit 0