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


def load_config(project_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    with open(config_path, "r") as f:
        configs = json.load(f)
        config = configs.get(project_name)

        if config:
            return config
        else:
            print(
                f"ERROR: config.json file not found for project {project_name}!"
            )


def run_shell_script(script_name, config):
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

    try:
        subprocess.run([script_path], env=env_vars, check=True, shell=True)
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
        choices=["ec2-sync", "s3-sync", "ec2-ssh"],
    )

    parser.add_argument(
        "project",
        help="The project name. Example: market-intelligence, sigma-website, ...",
    )

    args = parser.parse_args()
    config = load_config(args.project)  # Load config for the chosen project
    if args.command == "ec2-sync":
        run_shell_script("ec2-sync.sh", config)
        
    elif args.command == "s3-sync":
        run_shell_script("s3-sync.sh", config)
        
    elif args.command == "ec2-ssh":
        run_shell_script("ec2-ssh.sh", config)
    else:
        sys.stderr.write("ERROR: Invalid command\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
