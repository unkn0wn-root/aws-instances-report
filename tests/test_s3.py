import pytest
from tempfile import NamedTemporaryFile
from s3 import AWSS3Client

'''
This should be proper testing! For now it just tries to "mock" connection, create and list files created in bucket
but this should be real csv file etc. Because of very short timeframe - it what it is for now :)
'''
# Mock S3 client
@pytest.fixture
def test_s3_bucket():
    return "aws_test_bucket"

@pytest.fixture
def test_s3(test_s3_client, test_s3_bucket):
    test_s3_client.create_bucket(Bucket = test_s3_bucket)
    yield

def test_list_buckets(test_s3_client, test_s3):
    my_client = AWSS3Client()
    buckets = my_client.list_buckets()
    assert buckets == ["aws_test_bucket"]

def test_create_list_s3(test_s3_client, test_s3):
    '''
    temp files does not work on Windows. We could create our own class/func to create temp files with generators etc.
    but i wanted just to provide some simple mocking test functonality for now
    '''
    file_text = "mocking_s3"
    with NamedTemporaryFile(delete = True, suffix = ".csv") as tmp_file:
        with open(tmp_file.name, "w", encoding = "UTF-8") as f:
            f.write(file_text)
        
        test_s3_client.upload_file(tmp_file.name, "aws_test_bucket", "test_file1")
        test_s3_client.upload_file(tmp_file.name, "aws_test_bucket", "test_file2")
        test_s3_client.upload_file(tmp_file.name, "aws_test_bucket", "test_file3")

    mock_client = AWSS3Client()
    objs = mock_client.list_objects(bucket_name = "aws_test_bucket", prefix = "test_")
    assert objs == [
        "test_file1", 
        "test_file2", 
        "test_file3"
        ]

