# Purpose

Deploy simple lambda and instructions to test third party dependencies.

# Deployment

## Pre-requisites

Read [AWS instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) and understand how lambda works and what are limitations.

Make sure you have configured AWS profile. If you wish to execute python file from your local machine, your default AWS profile must have access to S3 buckets (read only).

Running lambda on AWS, requires at least a role with following permission: `AmazonS3ReadOnlyAccess`.

In order to identify right versions of third-party libraries to be installed, follow *Common issues* section of this readme.


### Prepare zip package with dependencies

Make sure you are on root folder of your repository.
1. `mkdir packages` to create `packages` folder to put your dependencies there.
2. `pip install --target packages/ requests==2.31.0 urllib3==1.26.16` to install dependencies in right versions
3. `cd packages && zip -r packackages.zip .` to zip all dependencies
4. `cd .. && zip packages.zip lambda_function.py` to add lambda python file to zip

### Deploy to AWS

`ws lambda create-function --function-name get-s3-new --zip-file fileb://packages.zip --runtime python3.9 --handler lambda_function.lambda_handler --role arn:aws:iam::XXXXXXXXXXXX:role/S3_ReadOnly_for_lambda`

* `--function-name` is your lambda function name
* `--handles` make sure your handler is in line with you python file name and handler function name
* `--role` use your created role name as explained in preconditions


# Common issues

## botocore and urllib3 compatibility issues

Let's assume you would like to add *requests* package to your zip file.

When you install your dependency packages into zip using `pip install --target
. requests` you may get following error: *botocore 1.29.155 requires
urllib3<1.27,>=1.25.4, but you have urllib3 2.0.3 which is incompatible.*

After consulting following articles:
* https://github.com/boto/botocore/issues/2963
* https://github.com/boto/botocore/issues/2926

I have added to my requirements-dev.txt file last row: `urllib3<2`.

To avoid further conflicts in python packages, after reading following
articles:
* https://pip.pypa.io/en/stable/topics/dependency-resolution/
* https://codingshower.com/pip-dependency-resolver-and-version-conflicts/
* https://medium.com/knerd/the-nine-circles-of-python-dependency-hell-481d53e3e025
* https://docs.divio.com/en/latest/how-to/debug-dependency-conflict/

I have installed following tools:
* pipdeptree (command: `deptree`)
* pip-tools (command: `pip-compile`)

I used primarily `pip-compile`, specifically command: `pip-compile -r -v
requirements.txt requirements-dev.txt --output-file results.txt`

This generated 'safe' result of dependencies in `results.txt`.

Then I used some part of this file to install 'safe' versions of the
dependencies for my lambda zip package:

But first to be on safe side, I have removed all previous packages:
`pip freeze | xargs pip uninstall -y`

Then I installed all safe packages using generated results.txt:
`pip install -r results.txt`

Then I installed required packages for my zip file:
`pip install --target . requests=2.31.0 urllib=1.26.16`
