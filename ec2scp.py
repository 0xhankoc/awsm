import subprocess
import sys
import json
import os


def load_config():
    # Load configuration from awsm_config.json at the repository root
    config_path = os.path.join(os.getcwd(), 'awsm_config.json')
    if not os.path.exists(config_path):
        print("Error: awsm_config.json not found in the current directory.")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def _ec2scp(ec2_user: str, ec2_address: str, pem_path: str, remote_path: str, local_path: str) -> None:
    """
    Download a file or directory from an EC2 instance to the local machine.

    :param ec2_user: EC2 username (e.g., ec2-user)
    :param ec2_address: Public DNS or IP of the EC2 instance
    :param pem_path: Path to the PEM key file
    :param remote_path: The remote file/folder path on EC2 instance to copy from
    :param local_path: The local destination path
    """
    scp_command = [
        "scp",
        "-r",  # to allow directory copying
        "-i", pem_path,
        f"{ec2_user}@{ec2_address}:{remote_path}",
        local_path
    ]

    result = subprocess.run(scp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)

    if result.returncode != 0:
        print("FAILED!")
        print(result.stderr)
        sys.exit(1)
    else:
        print(f"OK!")


def ec2scp(ec2_user, ec2_address, pem_path, remote_path, local_path):

    if not ec2_user or not ec2_address or not pem_path:
        print("Error: Missing required configuration in awsm_config.json (EC2_USER, EC2_ADDRESS, PEM_FILE_PATH).")
        sys.exit(1)

    print(f"Downloading {remote_path} from EC2 instance to {local_path}...")
    _ec2scp(ec2_user, ec2_address, pem_path, remote_path, local_path)

