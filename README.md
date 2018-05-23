# zabbix-aws-monitoring

This python module provides Zabbix monitoring support for AWS resources.

## Requirements

- Zabbix agent
- pip
- boto3 (installed automatically as dependency)

## Installation

1. Install the python module using pip.

```
pip install https://github.com/digiapulssi/zabbix-aws-monitoring/releases/download/1.0.0/aws-monitoring-1.0.0.tar.gz
```

2. Copy the Zabbix agent configuration to /etc/zabbix/zabbix_agentd.d directory.

3. Restart the Zabbix agent.

## Usage

### Discovery

Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.ecs.discover_services[region, access_key_id, secret_access_key, cluster_name] | Discover services in ECS cluster | {#CLUSTER_NAME}, {#NAME} |

### CloudWatch Metrics

See details on supported metrics at https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CW_Support_For_AWS.html

Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.cloudwatch.metric[region, access_key_id, secret_access_key, namespace, metric, dimensions, interval, statistic] | Retrieve cloudwatch metric | |

### S3 Bucket Metrics

*NOTE: Obtaining these metrics requires iterating all objects in bucket
which may be heavy operation depending on the number of objects.*

Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.s3.bucket_oldest[region, access_key_id, secret_access_key, bucket_name]
aws.s3.bucket_newest[region, access_key_id, secret_access_key, bucket_name]
aws.s3.bucket_size[region, access_key_id, secret_access_key, bucket_name]
