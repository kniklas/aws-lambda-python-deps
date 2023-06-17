# Purpose

Deploy simple lambda and instructions to test third party dependencies.

# Learning points

## botocore and urllib compatibility issues

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

and used primarily `pip-compile`, specifically command: `pip-compile -r -v
requirements.txt requirements-dev.txt --output-file results.txt`

This generated 'safe' result of dependencies in `results.txt`.

Then I used some part of this file to install 'safe' versions of the
dependencies for my lambda zip package:

But first to be on safe side, I have removed all previous packages:
`pip freeze | xargs pip uninstall -y`

Then I installed all safe packages using generated results.txt:
`pip install -r results.txt`

Then I installed required packages for my zip file:
`pip install --target . requests=2.31.0 urllib=1.26.16
