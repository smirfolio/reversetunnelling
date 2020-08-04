#!/bin/bash

currentDate=`date`
SERVER=$1

kill -9 $(ps aux | grep "[s]sh.*${SERVER}" | awk {'print $2'})
kill -9 $(ps aux | grep "[s]sh.*54321 localhost" | awk {'print $2'})
echo $currentDate ... Shut Down the tunelling