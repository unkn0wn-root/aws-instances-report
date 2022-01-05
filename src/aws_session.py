import boto3, botocore
from config import AWS_ACCESSKEY_ID, AWS_SECRETKEY, AWS_REGION


def aws_session(aws_key_id: str = AWS_ACCESSKEY_ID, 
                aws_secret: str = AWS_SECRETKEY, 
                region: str = AWS_REGION) -> boto3.Session:    
    if aws_key_id is None or aws_secret is None or region is None:
        raise ValueError("Either keyId, secret or region is not specified! Aborting...")
    # Check whatever boto3 is installed already in the system. If in docker so should already be specified inside dockerfile
    try:
        import boto3
    except ImportError:
        from pip._internal import main as pip
        pip(['install', '--user', 'boto3'])
        import boto3
    
    try:
        return boto3.Session(aws_access_key_id = aws_key_id, 
                            aws_secret_access_key = aws_secret, 
                            region_name = region)
    except botocore.exceptions.EndpointConnectionError as connection_error:
        # @TODO: Do something more when connection error. Retries? 
        print('Connection error to AWS')
        raise Exception(connection_error)
    except botocore.exceptions.ClientError as client_error:
        print(f"Client error on aws_session. Error: {client_error.message}")
        raise Exception(client_error)
    except Exception as err:
        raise err