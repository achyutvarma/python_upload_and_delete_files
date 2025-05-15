import os
import boto3
from botocore.exceptions import ClientError

# AWS Configuration
AWS_REGION = 'us-east-1'  # Change as per your region
BUCKET_NAME = 'your-s3-bucket-name'
S3_FOLDER = 'your/s3/folder/'  # Leave blank for root ex localfolders/

# Local folder path
LOCAL_FOLDER = '/path/to/your/local/folder'

# Initialize S3 client
s3 = boto3.client('s3', region_name=AWS_REGION)  # Initialize S3 client

def upload_and_delete_files(local_folder, bucket, s3_folder):
    for filename in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, filename)

        if os.path.isfile(local_file_path) and not filename.startswith('.'):     # Skips hidden files (like .DS_Store or .gitignore).
            s3_key = os.path.join(s3_folder, filename)  #  Constructs the **object key** in S3, which acts like a file path inside the bucket.
                                                           Again, make sure `s3_folder` does not start with `s3://`.

            try:
                print(f"Uploading {filename} to s3://{bucket}/{s3_key}")
                s3.upload_file(local_file_path, bucket, s3_key)

                # If upload succeeds, delete the file
                os.remove(local_file_path)
                print(f"Deleted local file: {filename}")

            except ClientError as e:
                print(f"Failed to upload {filename}: {e}")

# Run the automation
upload_and_delete_files(LOCAL_FOLDER, BUCKET_NAME, S3_FOLDER)
