#!/bin/bash
source koi

koiname=say.sh
koidescription="A script for saying things"

function hello {
    __addarg "-h" "--help" "help" "optional" "" "Greet a person by name"
    __addarg "" "name" "positionalvalue" "required" "" "The name of someone you like"
    __addarg "-s" "--salutation" "storevalue" "optional" "Hello" "The greeting to use"
    __addarg "-e" "--exclaim" "flag" "optional" "" "If included, greeting will be exclaimed"
    __parseargs "$@"

    local exclaim_text=
    if [[ $exclaim -eq 1 ]] ; then
        exclaim_text='!'
    fi

    echo "${salutation}, ${name}${exclaim_text}"
}

__koirun "$@"
