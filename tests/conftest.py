import pytest, os
import boto3
from moto import mock_s3

'''
Export mocking functions to be later available to other func inside test_s3
'''
@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "test_access_key123"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "123yek_ssecca_tset"

@pytest.fixture
def test_s3_client(aws_credentials):
    with mock_s3():
        connection = boto3.client("s3", region_name = "us-east-1")
        yield connection
