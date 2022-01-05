import log

from aws_session import aws_session
from botocore.exceptions import NoCredentialsError
from timeit import default_timer as timer
from datetime import timedelta

def s3_upload(file: str, bucket: str, s3_file) -> bool:
    logger = log.setup_logger('s3_info_log')
    
    create_session = aws_session()
    s3 = create_session.resource('s3')

    try:
        logger.info(f"Now trying to upload file: {file} to bucket: {bucket}")
        start_time = timer()
        s3.meta.client.upload_file(file, bucket, s3_file)
        end_time = timer()
        logger.info(f"Upload successful! Upload took: [{timedelta(seconds=end_time-start_time)}]")
        
        return True
    except FileNotFoundError as file_not_found:
        raise file_not_found
    except NoCredentialsError as no_credentials:
        raise no_credentials
    except:
        return False
        