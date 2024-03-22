#!/bin/bash

echo $PEM_FILE_PATH     # Path to your PEM file
echo $EC2_USER                # EC2 instance username (e.g., ec2-user, ubuntu)
echo $EC2_ADDRESS          # EC2 instance address (IP or DNS)

# args
echo $LOCAL_DIR_PATH
echo $REMOTE_DIR_PATH


# Existing variables
PEM_FILE_PATH="$PEM_FILE_PATH"       # Path to your PEM file
EC2_USER="$EC2_USER"                 # EC2 instance username (e.g., ec2-user, ubuntu)
EC2_ADDRESS="$EC2_ADDRESS"           # EC2 instance address (IP or DNS)

# args
LOCAL_DIR_PATH="$1"
REMOTE_DIR_PATH="$2"

# Validate necessary variables
if [ -z "$PEM_FILE_PATH" ] || [ -z "$EC2_USER" ] || [ -z "$EC2_ADDRESS" ] || [ -z "$REMOTE_DIR_PATH" ] || [ -z "$LOCAL_DIR_PATH" ]; then
    echo "Error: Missing required information."
    exit 1
fi

# Use SCP to copy the file from EC2 to local machine
scp -i "$PEM_FILE_PATH" "$EC2_USER@$EC2_ADDRESS:$REMOTE_DIR_PATH" "$LOCAL_DIR_PATH"

# Check the SCP exit status
if [ "$?" -ne "0" ]; then
    echo "Error: SCP failed."
    exit 1
fi

echo "File copied successfully to $LOCAL_DIR_PATH."
