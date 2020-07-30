#!/bin/bash

## The Home Computer information See the README.md
SERVER=#<Domain Name / fixe ip address>#
USER=#<User in the Home computer>#
PORT=#<Used port>#
TIMEOUT=#<A time out in second>#

## Accept these traffic from $SERVER =>  5900: Vnc client income request, 6666: Socks proxy http request, 4022: ssh income request
createShhTunnel() {
    ssh -fN -R5901:localhost:5901 -R6666:localhost:54321 -R4022:localhost:22 ${USER}@${SERVER} -p ${PORT} -o ConnectTimeout=15
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
   echo $currentDate ... Ssh tunnel Tunel already created.....
fi
}

verifySsh
