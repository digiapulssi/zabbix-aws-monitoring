# zabbix-aws-monitoring

This python module provides Zabbix monitoring support for AWS resources.

## Requirements

- Zabbix agent
- pip
- boto3 (installed automatically as dependency)

## Installation

1. Install the python module using pip.

```
pip install https://github.com/digiapulssi/zabbix-aws-monitoring/releases/download/1.0.13/aws-monitoring-1.0.13.tar.gz
```

2. Copy the [Zabbix agent configuration](etc/zabbix/zabbix_agentd.d/ic_aws.conf) to /etc/zabbix/zabbix_agentd.d directory.

3. Restart the Zabbix agent.

## Usage

### Discovery

Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.ecs.discover_services[region, access_key_id, secret_access_key, cluster_name] | Discover services in ECS cluster | {#CLUSTER_NAME}, {#SERVICE_NAME} |
aws.ecs.discover_tasks[region, access_key_id, secret_access_key, cluster_name, container_port] | Discover tasks in ECS cluster | {#TASKARN}, {#BINDIP} {#HOSTPORT} |
aws.rds.discover_db_instances[region, access_key_id, secret_access_key, cluster_identifier] | Discover instances in RDS cluster | {#DB_IDENTIFIER} |
aws.lambda.discover_functions[region, access_key_id, secret_access_key] | Discover Lambda functions | {#FUNCTIONNAME}, {#DESCRIPTION} |

### CloudWatch Metrics

See details on supported metrics at https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CW_Support_For_AWS.html

Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.cloudwatch.metric[region, access_key_id, secret_access_key, namespace, metric, interval, statistic, dimensions] | Retrieve cloudwatch metric | depends on metric |
aws.cloudwatch.metric.timeshift[region, access_key_id, secret_access_key, namespace, metric, interval, statistic, dimensions, timeshift] | Retrieve timeshifted cloudwatch metric | depends on metric |


Timeshift is specified in seconds

*Example:*

Number of messages within last hour in the SQS exampleQueue:
```
aws.cloudwatch.metric[eu-west-1, EXAMPLEACCESSKEY, ExampleSecretKey, AWS/SQS, NumberOfMessagesReceived, 3600, Sum, QueueName=exampleQueue
```

### S3 Bucket Metrics

*NOTE: Obtaining these metrics requires iterating all objects in bucket
which may be heavy operation depending on the number of objects.*

Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.s3.bucket_oldest[region, access_key_id, secret_access_key, bucket_name] | Age of oldest item in bucket | seconds |
aws.s3.bucket_newest[region, access_key_id, secret_access_key, bucket_name] | Age of newest item in bucket | seconds |
aws.s3.bucket_size[region, access_key_id, secret_access_key, bucket_name] | Total size of bucket | bytes |

### Other metrics

See details on supported methods and usage  at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html 

Currently only string optional arguments are supported. 


Item Syntax | Description | Units |
----------- | ----------- | ----- |
aws.query[region, access_key_id, secret_access_key, namespace, method, arguments] | Call a specified function in specified namespace | JSON |
Example: aws.query[{$REGION}, {$AWS_ACCESS_KEY_ID}, {$AWS_SECRET_ACCESS_KEY},application-autoscaling,describe_scalable_targets,"ServiceNamespace=ecs"]

Arguments can be given in two forms:
- String form: key1=value1,key2=value2,key3=value3
- List form: key1=/1,2,3/,key2=/4,5,6/,key3=/7,8,9/

Forward slashes are used instead of brackets because brackets are not allowed in Zabbix UserParameter keys.
