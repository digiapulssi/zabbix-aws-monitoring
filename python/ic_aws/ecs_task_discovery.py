#!/usr/bin/python

from argparse import ArgumentParser
from aws_client import AWSClient, add_aws_client_arguments
import json


class ECSTaskDiscovery(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()

    def find_tasks(self, cluster_name):

        tasks = self._client.list_tasks(
            cluster=cluster_name
        )
        task_descs_result = self._client.describe_tasks(
            cluster=cluster_name,
            tasks=tasks["taskArns"]
        )

        task_descs = []
        task_descs.extend(task_descs_result["tasks"])

        while "nextToken" in tasks:
            tasks = self._client.list_tasks(
                cluster=cluster_name,
                nextToken=tasks["nextToken"]
            )
            task_descs_result = self._client.describe_tasks(
                cluster=cluster_name,
                tasks=tasks["taskArns"]
            )
            task_descs.extend(task_descs_result["tasks"])

        return task_descs

    def find_network_bindings(self, task, container_port):
        network_bindings = []
        for container in task["containers"]:
            for network_binding in containers["networkBindings"]:
                if container_port == network_binding["containerPort"]:
                    network_bindings.append(network_binding)

        return network_bindings


def main(args=None):
    parser = ArgumentParser(description="Discover ECS services")
    add_aws_client_arguments(parser)

    parser.add_argument("cluster_name")
    parser.add_argument("container_port")

    args = parser.parse_args(args)

    aws_client = AWSClient("ecs", args)
    client = ECSTaskDiscovery(aws_client)
    task_descs = client.find_tasks(args.cluster_name)

    names = []
    for task in task_descs:
        for network_binding in client.find_network_bindings(task, args.container_port):
            names.append({
                "{#TASKARN}": task["taskArn"],
                "{#BINDIP}": network_binding["bindIP"],
                "{#HOSTPORT}": network_binding["hostPort"]
            })
    discovery = {"data": names}
    print json.dumps(discovery)


if __name__ == "__main__":
    main()
