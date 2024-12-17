# AWSM: AWS CLI Helper Tool

AWSM is a command-line helper tool designed to streamline routine AWS tasks like syncing local files with an EC2 instance or an S3 bucket, and establishing SSH connections with EC2 instances.

## 🚀 Installation

Before you start using AWSM, ensure you have Python and necessary modules installed on your machine.

```bash
git clone https://github.com/0xhankoc/awsm
cd awsm
pip install -r requirements.txt
```

### Configuring Path

Add `awsm` to your path in `.zshrc` or `.bashrc`:

```bash
export PATH="$PATH:/path-to-awsm-directory"
```

### Configurations

Create an `awsm_config.json` file in your project directory. 

Depending on which AWS infra (EC2 / S3) the project is using, fill out the
following fields in the project config file named `awsm_config.json`:
```json
{
  "CREDENTIALS": "/Users/orhankoc/.aws/sigma/root/orhankoc_accessKeys.csv",
  "EC2": {
    "EC2_USER": "ec2-user",
    "EC2_ADDRESS": "44.239.71.1",
    "PEM_FILE_PATH": "/Users/orhankoc/.aws/sigma/root/etl/orhan2.pem",
    "TARGET_DIR_PATH": "/home/ec2-user",
    "SOURCE_DIR_PATH": "/Users/orhankoc/Documents/850house/kaizen/kaizen-backend",
    "IGNORE_PATTERNS": ["assets/images/*", "node_modules/*", "logs/*"]
  }
}

```

## 🛠 Usage

AWSM supports the following commands:

### 1️⃣ Syncing with EC2

Synchronize your local project files with your EC2 instance.

```bash
awsm ec2-sync 
```

### 2️⃣ Syncing with S3

Synchronize your local project files with your S3 bucket.

```bash
awsm s3-sync
```

### 3️⃣ SSH into EC2

Establish an SSH connection with your EC2 instance.

```bash
awsm ec2-ssh
```

### 📜 Note

- Ensure your AWS credentials are configured properly in your environment to use AWS services.


## 🙌 Contributing
If you wish to contribute to this project, please fork the repository and submit a pull request!

## 📜 License
This project is licensed under the MIT License.

## 🙏 Acknowledgments
- Thanks to AWS for the versatile cloud services.
- Anyone who contributes to open-source projects!
```