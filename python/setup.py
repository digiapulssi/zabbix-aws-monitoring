import os
from setuptools import setup

setup(
    name="aws-monitoring",
    version="1.0.4",
    author="Sami Pajunen",
    author_email="sami.pajunen@digia.com",
    description="Monitoring scripts for AWS services",
    url="https://github.com/digiapulssi/zabbix-monitoring-scripts/",
    license="GPLv3",
    packages=['ic_aws'],
    entry_points={
        "console_scripts": [
            "aws_s3_bucket_stat = ic_aws.s3_bucket_stat:main",
            "aws_cloudwatch_metric = ic_aws.cloudwatch_metric:main",
            "aws_ecs_discovery = ic_aws.ecs_discovery:main",
            "aws_ecs_task_discovery = ic_aws.ecs_task_discovery:main",
            "aws_rds_discovery = ic_aws.rds_discovery:main"
        ]
    },
    install_requires=['boto3>=1.7.19']
)
