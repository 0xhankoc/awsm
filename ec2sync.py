import subprocess
from typing import List

DEFAULT_IGNORE_PATTERN = [
    ".git/",
    "venv/",
    "__pycache__/",
    "docs/",
    ".DS_STORE",
    "awsm_config.json"
]


def ec2sync(
        ec2_user: str,
        ec2_address: str,
        pem_path: str,
        source_directory_path: str,
        target_directory_path: str,
        ignore_patterns: List[str] = []
) -> None:
    # Combine default and provided ignore patterns
    all_ignore_patterns = ignore_patterns + DEFAULT_IGNORE_PATTERN
    # Convert ignore patterns into a list of '--exclude' arguments
    ignore_args = [f"--exclude={pattern}" for pattern in all_ignore_patterns]

    # Construct the rsync command as a list
    rsync_command = (
            [
                "rsync",
                "-avz",
                "--no-times",
                "--no-perms",
                "-e",
                f"ssh -i {pem_path}",
            ] + ignore_args + [
                source_directory_path,
                f"{ec2_user}@{ec2_address}:{target_directory_path}"
            ]
    )

    # Execute the command
    result = subprocess.run(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)

    if result.returncode != 0:
        print("Error: Rsync failed.")
        print(result.stderr)
        exit(1)
    else:
        print(f"Local state synced to {target_directory_path} on AWS EC2.")

