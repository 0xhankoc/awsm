#!/bin/bash

# Existing variables
PEM_FILE_PATH="$PEM_FILE_PATH"
EC2_USER="$EC2_USER"
REPO_DIR_NAME="$REPO_DIR_NAME"
APP_DIR_PATH="$APP_DIR_PATH"
REPO_DIR_PATH="$REPO_DIR_PATH"
EC2_ADDRESS="$EC2_ADDRESS"
GIT_REPO_URL="$GIT_REPO_URL" # Add your Git repository URL here

# Get the current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Validate the REPO_DIR_NAME
if [ -z "$REPO_DIR_NAME" ]; then
    echo "Error: Could not determine the repository directory name."
    exit 1
fi

# Check if the current branch is 'main'
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "You're not on the 'main' branch. Exiting."
  exit 1
fi

# Rsync local changes to EC2
rsync -avz -e "ssh -i $PEM_FILE_PATH" --exclude '.git/' --exclude 'venv/' --exclude '__pycache__/' --exclude 'docs/' "$REPO_DIR_PATH/$REPO_DIR_NAME" $EC2_USER@$EC2_ADDRESS:$APP_DIR_PATH

# Check the rsync exit status
if [ "$?" -ne "0" ]; then
    echo "Error: Rsync failed."
    exit 1
fi

echo "Local state synced to $REPO_DIR_NAME on AWS EC2."

# SSH into the EC2 instance and clone the Git repository
ssh -i $PEM_FILE_PATH $EC2_USER@$EC2_ADDRESS << EOF
  echo "Cloning Git repository into the EC2 instance..."
  if [ ! -d "$APP_DIR_PATH/$REPO_DIR_NAME" ]; then
    git clone $GIT_REPO_URL "$APP_DIR_PATH/$REPO_DIR_NAME"
  else
    echo "Repository already exists in the EC2 instance."
  fi
  exit
EOF

# Check the SSH and Git clone exit status
if [ "$?" -eq "0" ]; then
    echo "Git repository cloned into $REPO_DIR_NAME on AWS EC2."
else
    echo "Error: SSH into EC2 or Git clone failed."
    exit 1
fi
