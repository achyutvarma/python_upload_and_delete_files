# Updated Script with Retention Period Logic
This example uses a retention period of 1 day (24 hours). You can adjust it easily.

python
Copy
Edit
import os
import boto3
import time
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# AWS Configuration
AWS_REGION = 'eu-north-1'
BUCKET_NAME = 'newawwsbucket266666666'
S3_FOLDER = 'localfiles/'  # S3 key prefix, not s3://...

# Local folder path
LOCAL_FOLDER = '/home/ubuntu/local_folder'

# Retention period (in seconds)
RETENTION_PERIOD_SECONDS = 24 * 60 * 60  # 1 day

# Initialize S3 client
s3 = boto3.client('s3', region_name=AWS_REGION)

def upload_and_delete_files(local_folder, bucket, s3_folder):
    current_time = time.time()

    for filename in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, filename)

        if os.path.isfile(local_file_path) and not filename.startswith('.'):
            # Get file's last modified time
            file_mtime = os.path.getmtime(local_file_path)

            # Upload to S3
            s3_key = os.path.join(s3_folder, filename)

            try:
                print(f"Uploading {filename} to s3://{bucket}/{s3_key}")
                s3.upload_file(local_file_path, bucket, s3_key)

                # Only delete if older than retention period
                if current_time - file_mtime >= RETENTION_PERIOD_SECONDS:
                    os.remove(local_file_path)
                    print(f"Deleted local file: {filename}")
                else:
                    print(f"Skipped deleting {filename} (retention period not met)")

            except ClientError as e:
                print(f"Failed to upload {filename}: {e}")

# Run the automation
upload_and_delete_files(LOCAL_FOLDER, BUCKET_NAME, S3_FOLDER)
