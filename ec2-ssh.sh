#!/bin/bash

PEM_FILE_PATH="$PEM_FILE_PATH"
EC2_USER="$EC2_USER"
REPO_DIR_NAME="$REPO_DIR_NAME"
EC2_ADDRESS="$EC2_ADDRESS"

# Validate the REPO_DIR_NAME
if [ -z "$REPO_DIR_NAME" ]; then
    echo "Error: Could not determine the repository directory name."
    exit 1
fi

# Step 2: SSH into the EC2 instance and perform any additional actions if needed
ssh -t -t -i "$PEM_FILE_PATH" $EC2_USER@$EC2_ADDRESS

# Check if the SSH was successful
if [ $? -eq 0 ]; then
    echo "Sign in successful to $EC2_ADDRESS."
else
    echo "Sign in failed."
    exit 1
fi