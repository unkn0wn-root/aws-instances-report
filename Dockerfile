FROM python:3.9-alpine

ENV aws_access_key_id=
ENV aws_secret_key=
ENV aws_region=
ENV aws_bucket_name=

RUN apk update && apk add python3-dev gcc libffi-dev libc-dev

COPY . ./app

WORKDIR /app
RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["crond", "-f"]