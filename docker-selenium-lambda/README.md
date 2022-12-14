# Serverless lambda to pull studer data

This will connect with studer dashboard and pull daily data.

- Python 3.9.12
- chromium 102.0.5005.0
- chromedriver 102.0.5005.61
- selenium 4.2.0

## AWS Environment
- Root AWS account: solshare
- Region: ap-southeast-1

## Deploy and Run the lambda

```bash
$ npm install -g serverless # skip this line if you have already installed Serverless Framework
$ export AWS_REGION=ap-southeast-1 # You can specify region or skip this line. us-east-1 will be used by default.
$ cd docker-selenium-lambda
$ sls deploy
$ sls invoke --function demo # Yay! You will get texts of example.com
```
