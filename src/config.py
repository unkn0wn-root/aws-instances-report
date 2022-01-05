import os

from dotenv import load_dotenv
from pathlib import Path


# Try to load from .env file and if it doesn't exist - try to check for sys env.
env_file = os.path.join(f"{Path(__file__).parent.parent}/.env")
load_dotenv(env_file)
# AWS config
AWS_ACCESSKEY_ID = os.getenv('aws_access_key_id')
AWS_SECRETKEY = os.getenv('aws_secret_key')
AWS_REGION = os.getenv('aws_region')
AWS_S3_BUCKET = os.getenv('aws_bucket_name')

# test connection config
test_url = 'www.google.com'
test_port = 80