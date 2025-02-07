import os
import subprocess
import sys


def ec2ssh(ec2_user: str, ec2_address: str, pem_file_path: str):

    if not os.path.exists(pem_file_path):
        print(f"Error: The specified PEM file does not exist at '{pem_file_path}'.")
        sys.exit(1)

    # Construct the SSH command
    ssh_command = [
        "ssh",
        "-i", pem_file_path,
        f"{ec2_user}@{ec2_address}"
    ]

    result = subprocess.run(ssh_command, shell=False, check=True, text=True)

    if result.returncode == 0:
        print(f"Sign in successful to {ec2_address}.")
    else:
        print("Sign in failed.")
        print("Error output:")
        print(result.stderr)
        sys.exit(1)
