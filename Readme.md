# AWS RDS-EC2 Count & Export
Get and count AWS EC2 and RDS instances, export to CSV and upload to S3 bucket.

## Structure :open_file_folder:
### `src/...` :gear:

This is the source repository of modules/helpers etc.

### `csv/...` :gear:

Here will our CSV files live

### `logs/...` :gear:

Directory for logs

### `tests/...` :gear:

Mock testing of S3

## Getting started

First you need to set env. variables (see .env-example) as system vars or just create file named '.env' at the root of the project. Then you can either run pip directly inside your env. or use virtual python env. (or dockerfile to build image and run cron schedule - see crontab file):

## With dockerfile:

- `docker build . --tag="aws-instances-report"` - build docker container
- `docker run -d aws-instances-report` - run docker container
- `docker exec -it <name of container> sh ` - to access container and see logs etc.

## Without virtual env.:

- `pip install -r requirements.txt`

## With virtual env:

- `python -m pip install --user virtualenv` to install
- `python -m venv aws-instances-report` - to create v. env.
- `source aws-instances-report/bin/activate` - to activate
- `pip install -r requirements.txt` - to install all required pckgs.

## To run tests:

- `cd ./tests && python -m pytest test_s3.py`

## To run application:

- `python app.py`

### Todo as for  07.11.2021 :construction_worker:

- [x] Add mock S3 tests
- [ ] Add EC2 and RDS tests
- [x] Docker file
- [x] Schedule via crontab
- [ ] Try to implement schedule via subprocesses instead of crontab
- [x] Add errors logging to file