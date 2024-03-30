import os
import subprocess

# Define paths and variables
S3_BUCKET = os.getenv('S3_BUCKET')
REPO_DIR_PATH = os.getenv('LOCAL_DIR_PATH')


def s3sync():
    sync_command = f'aws s3 sync {REPO_DIR_PATH} s3://{S3_BUCKET}/'
    result = subprocess.run(sync_command, shell=True)

    if result.returncode == 0:
        print(f'Main branch synced to the S3 Bucket {S3_BUCKET}!')
    else:
        print('S3 Sync failed.')
        exit(1)
