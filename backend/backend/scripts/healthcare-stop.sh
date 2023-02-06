#!/bin/bash

pid=lsof -t -i:8080
if [ "$pid" != "" ]
then # Kill the running process
kill -9 $pid 2>/dev/null || :
fi
