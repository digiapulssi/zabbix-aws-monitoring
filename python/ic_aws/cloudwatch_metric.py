#!/usr/bin/python

from datetime import datetime, timedelta
from argparse import ArgumentParser
from aws_client import AWSClient, add_aws_client_arguments


class CloudWatchMetric(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()

    def get_metric(self, interval, metric, namespace, statistic, dimensions,
                   timeshift):
        end_time = datetime.utcnow() - timedelta(seconds=timeshift)
        start_time = end_time - timedelta(seconds=interval)
        result = self._client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric,
            Dimensions=dimensions,
            StartTime=start_time.isoformat(),
            EndTime=end_time.isoformat(),
            Statistics=[statistic],
            Period=interval
        )
        if len(result["Datapoints"]) > 0:
            ret_val = result["Datapoints"][0][statistic]
        else:
            ret_val = -1
        return ret_val


def main(args=None):
    parser = ArgumentParser(description="Retrieve AWS CloudWatch metrics")
    add_aws_client_arguments(parser)

    parser.add_argument("--timeshift", type=int, default=0,
                        help="Time shift for interval")

    parser.add_argument("namespace", help="AWS namespace. e.g. AWS/ECS")
    parser.add_argument("metric", help="Metric to obtain")
    parser.add_argument("interval", type=int, help="Statistic interval")
    parser.add_argument("statistic", help="Statistic to retrieve. e.g. Sum")
    parser.add_argument("dimensions", help="Dimension filter")

    args = parser.parse_args(args)

    dimensions = list()
    for dimension in args.dimensions.split(","):
        instance = dimension.split("=")
        dimensions.append(dict(zip(("Name", "Value"), instance)))

    aws_client = AWSClient("cloudwatch", args)
    client = CloudWatchMetric(aws_client)
    value = client.get_metric(args.interval, args.metric, args.namespace,
                              args.statistic, dimensions, args.timeshift)
    if value == -1:
        print("")
    else:
        print(value)


if __name__ == "__main__":
    main()
