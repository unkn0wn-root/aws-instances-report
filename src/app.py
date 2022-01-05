import sys
sys.path.append('src')

import datetime
import log

from pathlib import Path
from aws_session import aws_session
from collections import Counter

try:
    from prettytable import PrettyTable
except ImportError:
    from pip._internal import main as pip
    pip(['install', '--user', 'PrettyTable'])
    from prettytable import PrettyTable

# create logs dir if not exist
Path('../logs').mkdir(exist_ok=True)
# error log goes to both stdout and stream (file)
err_log_path = f"../logs/main_error_{datetime.datetime.now().strftime('%Y_%m_%d')}.log"
err_logger = log.setup_logger('main_error_log', err_log_path, 'ERROR')
# only print to console for info logging
info_logger = log.setup_logger('main_info_log')

'''
@TODO: be more specific about what type of errors you want to catch and do diffrent things based on that.
'''
def ec2_task() -> dict:
    info_logger.info("Running EC2 task now...")

    try:
        '''
        Connect using session module defined in aws_session.py which throws if something goes wrong
        then get instances types and count each element in list.
        @returns dict
        '''
        current_ec2_session = aws_session()
        ec2_session = current_ec2_session.resource('ec2')
        # store instances types here
        ec2_types_list = [ec2_instance.instance_type for ec2_instance in ec2_session.instances.all()]
        ec2_types_count = dict(Counter(ec2_types_list))

        tab = PrettyTable(['Source', 'Type', 'Count'])
        for key, value in ec2_types_count.items():
            tab.add_row(['ec2', key, value])
        print(tab)
        
        return ec2_types_count
    except Exception as error:
        err_logger.error(error)
        raise error

def rds_task() -> dict:
    info_logger.info("Running AWS RDS task now...")

    try:
        current_rds_session = aws_session()
        rds_session = current_rds_session.client('rds')
        # store rds instances types
        rds_types_list = [rds_instance['DBInstanceClass'] for rds_instance in rds_session.describe_db_instances()['DBInstances']]
        rds_types_count = dict(Counter(rds_types_list))

        tab = PrettyTable(['Source', 'Type', 'Count'])
        for key, value in rds_types_count.items():
            tab.add_row(['rds', key, value])
        print(tab)

        return rds_types_count
    except Exception as error:
        err_logger.error(error)
        raise error


if __name__ == '__main__':
    import sys
    sys.path.append('src')
    
    import csv

    from s3 import s3_upload
    from config import AWS_S3_BUCKET
    from pathlib import Path
    from helpers import check_connection
    from config import test_url, test_port

    # ensure that we have an active internet conn. Log and abort if we can't verify . No need to go to next step if this fails
    try:
        test_connection = check_connection(test_url, test_port)
        if test_connection:
            print("\N{rocket}", 'We have internet connection! Proceed with script...')
        else:
            raise ConnectionError('Something went wrong... Could not verify if connection to internet is valid. Aborting...')
    except Exception as err:
        err_logger.error(err)
        exit(1)

    try:
        csv_file_timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        csv_file_name = f"aws_count_services_{csv_file_timestamp}.csv"
        csv_file = f"../csv/{csv_file_name}"
        # create csv dir if not exists already
        Path('../csv').mkdir(exist_ok=True)
        # runs both tasks here
        get_ec2_types, get_rds_types = ec2_task(), rds_task()
        # adding multiple rows to file will add new empty line for each row so newline='' means no new line
        with open(csv_file, 'w+', encoding = 'UTF8', newline = '') as write_csv:
            write = csv.writer(write_csv)
            # headers
            write.writerow(['Source', 'Type', 'Count'])
            # write from ec2 and rds to csv file
            [write.writerow(['ec2', ec2_type, ec2_count]) for ec2_type, ec2_count in get_ec2_types.items()]
            [write.writerow(['rds', rds_type, rds_count ]) for rds_type, rds_count in get_rds_types.items()]
        # Upload to S3 and just log if this fails. We still have results so no need to stop everything
        try:
            upload_to_s3 = s3_upload(csv_file, AWS_S3_BUCKET, csv_file_name)
        except Exception as s3_error:
            err_logger.error(f"Something went wront with upload to S3! {s3_error}")
    except IOError as io_error:
        err_logger.error('File not found or could not be opened')
    except Exception as error:
        err_logger.error(error)
        