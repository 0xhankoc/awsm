"""
This file is the main script for the rest of the shell scripts included in
this repository. The scripts are used as shortcuts for common AWS actions.
Used for CI/CD.
"""
import os
import argparse
import sys
import json
import csv

from ec2sync import ec2sync
from ec2ssh import ec2ssh
from s3sync import s3sync
from ec2scp import ec2scp

AWSM_ROOT_PATH = os.path.abspath(__file__)
PROJECT_ROOT_PATH = os.getcwd()

def print_usage():
    print("""
Usage: awsm [command] [args...]

Available commands:
  ec2-sync         Sync local files to EC2 instance
  s3-sync          Sync local files with S3 bucket
  ec2-ssh          SSH into EC2 instance
  ec2-scp          Download files/folders from EC2 to local

Examples:
  awsm ec2-sync
  awsm s3-sync
  awsm ec2-ssh
  awsm ec2-scp [REMOTE_PATH] [LOCAL_PATH]
""")


def _aws_credentials(credentials_path):
    with open(credentials_path, mode='r') as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        # Extract credentials
        aws_access_key_id, aws_secret_access_key = next(reader)
        return aws_access_key_id.strip(), aws_secret_access_key.strip()


def _awsm_config(project_directory):
    # List of potential paths for the configuration file
    possible_paths = [
        os.path.join(project_directory, "awsm_config.json"),
        os.path.join(project_directory, "configs", "awsm_config.json")
    ]
    
    # Iterate through the list of possible paths
    for path in possible_paths:
        try:
            with open(path, "r") as f:
                # Return the config if found
                config = json.load(f)
                return config
        except FileNotFoundError:
            # Continue to next path if file is not found
            continue

    # If no file is found after all attempts, print error and exit
    print(f"ERROR: Unable to find awsm_config.json in specified paths.")
    sys.exit(1)


def _script_of_command(script_name: str) -> str:
    return os.path.join(AWSM_ROOT_PATH, script_name)


def main():

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    parser = argparse.ArgumentParser(
        description="AWSM: AWS CLI Helper Tool"
    )

    parser.add_argument(
        "command",
        help="The command to execute. Example: ec2sync, s3sync, ec2ssh, ...",
        choices=["ec2-sync", "s3-sync", "ec2-ssh", "ec2-scp"],
    )

    parser.add_argument(
        "remote_path",
        nargs='?',
        help="The remote file/folder path on EC2 instance to copy from (required for ec2-scp)"
    )

    parser.add_argument(
        "local_path",
        nargs='?',
        help="The local destination path (required for ec2-scp)"
    )

    args = parser.parse_args()
    config = _awsm_config(PROJECT_ROOT_PATH)

    if args.command=='ec2-ssh':
        ec2ssh(
            config['EC2']['EC2_USER'],
            config['EC2']['EC2_ADDRESS'],
            config['EC2']['PEM_FILE_PATH']
        )
    elif args.command=='ec2-sync':
        ec2sync(
            config['EC2']['EC2_USER'],
            config['EC2']['EC2_ADDRESS'],
            config['EC2']['PEM_FILE_PATH'],
            config['EC2']['SOURCE_DIR_PATH'],
            config['EC2']['TARGET_DIR_PATH'],
            config['EC2']['IGNORE_PATTERNS']
        )
    elif args.command=='s3-sync':
        s3sync(
            config['S3']['BUCKET_NAME'],
            config['S3']['LOCAL_DIR_PATH']
        )
    elif args.command=='ec2-scp':
        ec2scp(
            config['EC2']['EC2_USER'],
            config['EC2']['EC2_ADDRESS'],
            config['EC2']['PEM_FILE_PATH'],
            args.remote_path,
            args.local_path
        )
    else:
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
