#!/bin/bash

# Define paths and variables

S3_BUCKET="$S3_BUCKET"
REPO_DIR_PATH="$REPO_DIR_PATH"

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Check if the current branch is 'main'
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "You're not on the 'main' branch. Exiting."
  exit 1
fi

# Sync the directory with the S3 bucket
aws s3 sync $REPO_DIR_PATH s3://$S3_BUCKET/

# Check if the sync was successful
if [ $? -eq 0 ]; then
    echo ""Main branch synced to the S3 Bucket $S3_BUCKET!""
else
    echo "S3 Sync failed."
    exit 1
fi