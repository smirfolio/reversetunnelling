#!/bin/bash


# Make a local http socks 

createSshProxyLocal() {
    ssh -fN -D 54321 localhost
    if [[ $? -eq 0 ]]; then
        echo ssh localProxy  created successfully
    else
        echo An error occurred creating a localProxy $?
    fi
}

## Check Tunelling conections , then create a new connection
currentDate=`date`

verifySshlocalProxy(){
    ps aux | grep '[s]sh.*fN -D 54321'
if [[ $? -ne 0 ]]; then
    echo $currentDate ... Creating new localProxy
    createSshProxyLocal
else
   echo $currentDate ... localProxy already created.....
fi
}

verifySshlocalProxy