Absolutely, you can directly copy and paste the following markdown for your `README.md`:


# AWSM: AWS CLI Helper Tool

AWSM is a command-line helper tool designed to streamline routine AWS tasks like syncing local files with an EC2 instance or an S3 bucket, and establishing SSH connections with EC2 instances.

## 🚀 Installation

Before you start using AWSM, ensure you have Python and necessary modules installed on your machine.

```bash
git clone <your-repo-link>
cd awsm
pip install -r requirements.txt
```

### Configuring Path

Add `awsm` to your path in `.zshrc` or `.bashrc`:

```bash
export PATH="$PATH:/path-to-awsm-directory"
```

### Configurations

Ensure your configurations for each project are in `config.json` within the `awsm` directory.

Example `config.json`:

```json
{
  "market-intelligence": {
    "PEM_FILE_PATH": "/path/to/pem/file",
    "EC2_USER": "ec2-user",
    "REPO_DIR_NAME": "repo-dir-name",
    "APP_DIR_PATH": "/app/dir/path",
    "REPO_DIR_PATH": "/repo/dir/path",
    "EC2_ADDRESS": "ec2-address"
  }
  ...
}
```

## 🛠 Usage

AWSM supports the following commands:

### 1️⃣ Syncing with EC2

Synchronize your local project files with your EC2 instance.

```bash
awsm ec2-sync [project-name]
```

### 2️⃣ Syncing with S3

Synchronize your local project files with your S3 bucket.

```bash
awsm s3-sync [project-name]
```

### 3️⃣ SSH into EC2

Establish an SSH connection with your EC2 instance.

```bash
awsm ec2-ssh [project-name]
```

### 📜 Note

- Replace `[project-name]` with the actual project name defined in `config.json`.
- Ensure your AWS credentials are configured properly in your environment to use AWS services.

## 🧐 Troubleshooting & FAQ

**Q:** I'm encountering a "No such file or directory" error.

**A:** Ensure all file paths in your `config.json` are correct and that the respective files exist.

_For more FAQ and Troubleshooting, refer to the [FAQ](link-to-faq-page) section in our wiki._

## 🙌 Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request!

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Thanks to AWS for the versatile cloud services.
- Anyone who contributes to open-source projects!
```

Feel free to tailor the content per your project's specific requirements and details.