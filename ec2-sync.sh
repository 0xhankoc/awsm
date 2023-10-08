#!/bin/bash

PEM_FILE_PATH="$PEM_FILE_PATH"
EC2_USER="$EC2_USER"
REPO_DIR_NAME="$REPO_DIR_NAME"
APP_DIR_PATH="$APP_DIR_PATH"
REPO_DIR_PATH="$REPO_DIR_PATH"
EC2_ADDRESS="$EC2_ADDRESS"

# Validate the REPO_DIR_NAME
if [ -z "$REPO_DIR_NAME" ]; then
    echo "Error: Could not determine the repository directory name."
    exit 1
fi

# Rsync local changes to EC2
rsync -avz -e "ssh -i $PEM_FILE_PATH" --exclude '.git/' --exclude 'venv/' --exclude '__pycache__/' --exclude 'docs/' "$REPO_DIR_PATH/$REPO_DIR_NAME" $EC2_USER@$EC2_ADDRESS:$APP_DIR_PATH

# Check the rsync exit status and output accordingly
if [ "$?" -eq "0" ]; then
    echo "Local state synced to $REPO_DIR_NAME on AWS EC2."
else
    echo "Error: Rsync failed."
    exit 1
fi
