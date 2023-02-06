#!/bin/bash

HOME_PATH="/opt/codedeploy-agent/deployment-root"
SUFFIX="deployment-archive"

SERVICE="service"
SERVICE_PATH="/healthcare"
LOCAL_PREFIX="$HOME_PATH/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/$SUFFIX"
CODE_PATH="$LOCAL_PREFIX/$SERVICE"

# COPY_FILES="$CODE_PATH/."

SOURCE_FILE="raw_data.py"
REQ_FILE="requirements.txt"

SOURCE_PATH="$CODE_PATH/$SOURCE_FILE"
REQ_PATH="$CODE_PATH/$REQ_FILE"
FRESH_REQ_PATH="$SERVICE_PATH/$REQ_FILE"

ARTIFACT="backend.zip"
ARTIFACT_PATH="$HOME_PATH/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/$SUFFIX/$ARTIFACT"

if [ ! -d "/healthcare" ]
then
	sudo mkdir /healthcare
fi

sudo pwd
#sudo unzip -o $ARTIFACT_PATH -d $LOCAL_PREFIX

sudo cp  $SOURCE_PATH $SERVICE_PATH
sudo cp  $REQ_PATH $SERVICE_PATH

sudo pip3 install -r $FRESH_REQ_PATH
