#!/bin/bash

SERVICE_PATH="/healthcare"
SOURCE="raw_data.py"
SOURCE_PATH="$SERVICE_PATH/$SOURCE"

python3 $SOURCE_PATH >/dev/null 2>&1 &
