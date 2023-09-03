import boto3  # Importing the boto3 library, which provides an interface for interacting with AWS services.

class S3FileManager:
    def __init__(self):
        """
        Initializes an S3FileManager object, setting up a connection to the Amazon S3 service using boto3.
        You may need to provide aws_access_key_id and aws_secret_access_key if not using AWS CLI configuration.
        """
        self.s3 = boto3.client('s3')

    def upload_file(self, local_path, bucket_name, s3_path):
        """
        Uploads a file from the local file system to an Amazon S3 bucket.

        Parameters:
        - local_path (str): The path to the local file to be uploaded.
        - bucket_name (str): The name of the S3 bucket to upload the file to.
        - s3_path (str): The desired path for the file in the S3 bucket.

        Prints a success message upon successful upload or an error message if the upload fails.
        """
        try:
            self.s3.upload_file(local_path, bucket_name, s3_path)
            print(f'Successfully uploaded {local_path} to {s3_path}')
        except Exception as e:
            print(f'Error uploading {local_path} to {s3_path}: {e}')

    def download_file(self, bucket_name, s3_path, local_path):
        """
        Downloads a file from an Amazon S3 bucket to the local file system.

        Parameters:
        - bucket_name (str): The name of the S3 bucket containing the file.
        - s3_path (str): The path of the file in the S3 bucket.
        - local_path (str): The path where the file will be saved locally.

        Prints a success message upon successful download or an error message if the download fails.
        """
        try:
            self.s3.download_file(bucket_name, s3_path, local_path)
            print(f'Successfully downloaded {s3_path} to {local_path}')
        except Exception as e:
            print(f'Error downloading {s3_path} to {local_path}: {e}')

    def list_files(self, bucket_name, prefix=''):
        """
        Lists files in an Amazon S3 bucket with an optional prefix filter.

        Parameters:
        - bucket_name (str): The name of the S3 bucket to list files from.
        - prefix (str, optional): A prefix to filter files by path within the bucket.

        Returns a list of file paths or an empty list if there are no matching files.

        Prints an error message if listing files encounters an issue.
        """
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
