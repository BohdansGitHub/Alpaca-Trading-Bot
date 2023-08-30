import boto3


class S3FileManager:
    def __init__(self):
        self.s3 = boto3.client('s3')  # Add aws_access_key_id, aws_secret_access_key if you prefer not to use AWS CLI

    def upload_file(self, local_path, bucket_name, s3_path):
        try:
            self.s3.upload_file(local_path, bucket_name, s3_path)
            print(f'Successfully uploaded {local_path} to {s3_path}')
        except Exception as e:
            print(f'Error uploading {local_path} to {s3_path}: {e}')

    def download_file(self, bucket_name, s3_path, local_path):
        try:
            self.s3.download_file(bucket_name, s3_path, local_path)
            print(f'Successfully downloaded {s3_path} to {local_path}')
        except Exception as e:
            print(f'Error downloading {s3_path} to {local_path}: {e}')

    def list_files(self, bucket_name, prefix=''):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if 'Contents' in response:
                files = [obj['Key'] for obj in response['Contents']]
                return files
            else:
                return []
        except Exception as e:
            print(f'Error listing files in {bucket_name}/{prefix}: {e}')
            return []
