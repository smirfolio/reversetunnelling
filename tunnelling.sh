#!/bin/bash

## The Home Computer information See the README.md and the config.ini
SERVER=$1
USER=$2
PORT=$3
TIMEOUT=$4

## Accept these traffic from $SERVER =>  5900: Vnc client income request, 6666: Socks proxy http request, 4022: ssh income request
createShhTunnel() {
    ssh -fN -R5901:localhost:5901 -R6666:localhost:54321 -R4022:localhost:22 ${USER}@${SERVER} -p ${PORT} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=${TIMEOUT}
    if [[ $? -eq 0 ]]; then
        echo ssh Tunnel to host  created successfully
    else
        echo An error occurred creating a tunnel to host !!!
    fi
}

## Check Tunelling conections , then create a new connection
currentDate=`date`

verifySsh(){
    ps aux | grep "[s]sh.*${SERVER}"
if [[ $? -ne 0 ]]; then
    echo $currentDate ... Try to creating new ssh tunnel connection
    createShhTunnel
else
   echo $currentDate ... ssh tunnel Tunel already created.....
fi
}

verifySsh
