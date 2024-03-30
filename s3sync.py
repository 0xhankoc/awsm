import subprocess


def s3sync(S3_BUCKET, LOCAL_DIR_PATH):
    sync_command = f'aws s3 sync {LOCAL_DIR_PATH} s3://{S3_BUCKET}/'
    result = subprocess.run(sync_command, shell=True)

    if result.returncode == 0:
        print(f'Main branch synced to the S3 Bucket {S3_BUCKET}!')
    else:
        print('S3 Sync failed.')
        exit(1)
