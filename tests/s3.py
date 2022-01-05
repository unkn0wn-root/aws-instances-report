import boto3

class AWSS3Client:
    def __init__(self, region_name = "us-east-1"):
        self.client = boto3.client("s3", region_name = region_name)

    def list_objects(self, bucket_name, prefix):
        # Returns a list all objects with specified prefix
        response = self.client.list_objects(
            Bucket = bucket_name,
            Prefix = prefix,
        )
        return [object["Key"] for object in response["Contents"]]

    def list_buckets(self):
        # Returns bucket
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]