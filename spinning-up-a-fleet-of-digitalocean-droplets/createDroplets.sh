#!/bin/bash
set -e

function create {
    fingerprint="$(ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub | awk '{print $2}' | cut -c 5-)"
    for index in $(seq 1 ${1:-10}) ; do
        echo "Creating droplet-${index}"
        continue
        doctl compute droplet create "dropet-${index}" \
            --size s-1vcpu-1gb --image ubuntu-18-04-x64 \
            --region sfo2 \
            --format ID \
            --no-header \
            --ssh-keys $fingerprint
    done
    wait
}

function wait {
    complete=0
    while [[ complete -eq 0 ]] ; do
        complete=1
        ran=0
        statuses=( `doctl compute droplet list --no-header --format "Status"` )
        for status in "${statuses[@]}" ; do
            if [[ "$status" != active ]] ; then complete=0 ; fi
            ran=1
        done
        if [[ $ran -eq 0 ]] ; then complete=0 ; fi
    done
}

function run {
    for index in $(seq 1 ${1:-10}) ; do
        echo -n "Starting droplet-$index"
        
        doctl compute ssh "droplet-$index" --ssh-port 22 <<EndSSH > /dev/null 2>&1
cat << EndOfScript > run.sh
telnet towel.blinkenlights.nl
EndOfScript
EndSSH
        doctl compute ssh "droplet-$index" --ssh-command "\
            chmod +x ~/run.sh ; \
            echo '~/run.sh &' | script 'screen -' \
        " > /dev/null 2>&1
        echo "Started the job on droplet-$index"
    done
}

create

