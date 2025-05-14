# python_upload_and_delete_files
Python script That copies file from a folder in local dire to s3 bucket and deletes from this local.

Using AWS EC2 (General Purpose & Larger Files)
Use this for larger scripts or when more control and computing power is needed.

 Step 1: Create an IAM Role with S3 Permissions
Go to the IAM Console: https://console.aws.amazon.com/iam/

In the sidebar, click Roles → Create role.

Choose trusted entity:

Select AWS service

Use case: Choose EC2

Click Next

Attach permissions policies:

Search for and select AmazonS3FullAccess (or create a custom policy if needed)

Click Next

Name the role:

Example: EC2_S3_Access_Role

(Optional) Add a description

Click Create Role

✅ Step 2: Attach the Role to Your EC2 Instance
Go to the EC2 Console: https://console.aws.amazon.com/ec2/

In the left menu, click Instances.

Select your EC2 instance.

Choose Actions → Security → Modify IAM Role.

In the dropdown, select the role you just created (EC2_S3_Access_Role).

Click Update IAM Role.

✅ Step 3: Confirm Role Access from EC2
SSH into your instance and run:


aws sts get-caller-identity
You should see an IAM Role ARN that confirms the role is attached.

Then test S3 access:

aws s3 ls s3://your-s3-bucket-name

✅ Step 4:Install Python and Boto3 if not available:

sudo yum update -y
sudo yum install python3 -y
pip3 install boto3

Create your script on the instance 
vim upload_and_delete_files.py    #Enter the code here

✅ Step 5: Install aws cli using below commands
# 1. Update packages
sudo apt update

# 2. Install required dependencies
sudo apt install unzip curl -y

# 3. Download the AWS CLI v2 installer
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# 4. Unzip the installer
unzip awscliv2.zip

# 5. Run the installer
sudo ./aws/install

# 6. Verify the installation
aws --version
✅ Step 6:
Then you can run command 
python3 upload_and_delete_files.py #This runs the script and does the task mentioned in script (But Here we have to run the command manually).

✅ Step 7:To automate it fully there are different methods like you can use python library like watchdog,Use systemd service (Linux),Use crontab @reboot or a background process using tmux or screen

Here we used systemd service below is the process we followed.

Create a service file, e.g., /etc/systemd/system/s3-watcher.service

sudo nano /etc/systemd/system/s3-watcher.service

[Unit]
Description=Watch local folder and upload to S3
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/ubuntu/automation.py
WorkingDirectory=/home/ubuntu
Restart=always
RestartSec=5
User=ubuntu
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

Enter this in above service file.

Reload systemd and start the service:

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable s3-watcher.service
sudo systemctl start s3-watcher.service

Check status and logs

sudo systemctl status s3-watcher.service
journalctl -u s3-watcher.service -f

Note:Make sure you run in non root user (if you want to run as root user make required changes in script and above commands)




