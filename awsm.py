"""
This file is the main script for the rest of the shell scripts included in
this repository. The scripts are used as shortcuts for common AWS actions.
Used for CI/CD.
"""
import csv
import os
import argparse
import subprocess
import sys
import json

def extract_credentials(credentials_path):
    with open(credentials_path, mode='r') as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        # Extract credentials
        aws_access_key_id, aws_secret_access_key = next(reader)
        return aws_access_key_id.strip(), aws_secret_access_key.strip()


def load_config(current_dir):
    
    config_path = os.path.join(current_dir, "awsm_config.json")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print(f"ERROR: Unable to find awsm_config.json in the current working directory.")
        sys.exit(1)


def run_shell_script(script_name, config, extra_args=None):
    aws_access_key_id, aws_secret_access_key = extract_credentials(config['credentials'])
    env_vars = os.environ.copy()
    env_vars['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    env_vars['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
    
    # If EC2 config is present, pass those as well
    ec2_config = config.get('ec2')
    if ec2_config:
        for key, value in ec2_config.items():
            env_vars[key.upper()] = value
    
    # If S3 config is present, pass those as well
    s3_config = config.get('s3')
    if s3_config:
        for key, value in s3_config.items():
            env_vars[key.upper()] = value
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    command = [script_path] + extra_args if extra_args else [script_path]
    command = ' '.join(command)
    
    #command = [script_path]
    #if extra_args:
    #    command.extend(extra_args)

    try:
        subprocess.run(command, env=env_vars, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error executing {script_name}: {str(e)}\n")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Helper script to execute different actions."
    )
    parser.add_argument(
        "command",
        help="The command to execute. Example: ec2-sync, s3-sync, ec2-ssh, ...",
        choices=["ec2-sync", "s3-sync", "ec2-ssh", "ec2-scp"],
    )

    if 'ec2-scp' in sys.argv:
        parser.add_argument("LOCAL_DIR_PATH", help="Local directory path for the scp command")
        parser.add_argument("REMOTE_DIR_PATH", help="Remote directory path for the scp command")

    args = parser.parse_args()
    config = load_config(os.getcwd())  # Load config in the current directory
    if args.command == "ec2-sync":
        run_shell_script("ec2-sync.sh", config)
    elif args.command == "s3-sync":
        run_shell_script("s3-sync.sh", config)
    elif args.command == "ec2-ssh":
        run_shell_script("ec2-ssh.sh", config)
    elif args.command == "ec2-scp":
        extra_args = [args.LOCAL_DIR_PATH, args.REMOTE_DIR_PATH]
        run_shell_script("ec2-scp.sh", config, extra_args)
    else:
        sys.stderr.write("ERROR: Invalid command\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
