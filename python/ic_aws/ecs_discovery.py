#!/usr/bin/env python

from argparse import ArgumentParser
from ic_aws.aws_client import AWSClient, add_aws_client_arguments
import json


class ECSDiscovery(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()

    def find_services(self, cluster_name):

        services = self._client.list_services(
            cluster=cluster_name
        )

        serviceArns = []
        serviceArns.extend(services["serviceArns"])

        while "nextToken" in services:
            services = self._client.list_services(
                cluster=cluster_name,
                nextToken=services["nextToken"]
            )
            serviceArns.extend(services["serviceArns"])

        return serviceArns


def main(args=None):
    parser = ArgumentParser(description="Discover ECS services")
    add_aws_client_arguments(parser)

    parser.add_argument("cluster_name")

    args = parser.parse_args(args)

    aws_client = AWSClient("ecs", args)
    client = ECSDiscovery(aws_client)
    serviceArns = client.find_services(args.cluster_name)

    names = []
    for arn in serviceArns:
        names.append({
                "{#CLUSTER_NAME}": args.cluster_name,
                "{#SERVICE_NAME}": arn.split("/")[-1]
            })
    discovery = {"data": names}
    print(json.dumps(discovery))


if __name__ == "__main__":
    main()
