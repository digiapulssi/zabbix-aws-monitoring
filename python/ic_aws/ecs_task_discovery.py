#!/usr/bin/python3

from argparse import ArgumentParser
from aws_client import AWSClient, add_aws_client_arguments
import json


class ECSTaskDiscovery(object):
    def __init__(self, aws_client, ec2_client):
        self._client = aws_client.client()
        self._ec2_client = ec2_client.client()

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

    def find_network_bindings(self, task, container_port, cluster_name):
        network_bindings = []
        instances = self.find_instances(cluster_name, task["containerInstanceArn"])
        for container in task["containers"]:
            for network_binding in container["networkBindings"]:
                if container_port == str(network_binding["containerPort"]):
                    for instance in instances:
                        network_bindings.append([network_binding, instance["PrivateIpAddress"]])
        return network_bindings

    def find_instances(self, cluster_name, container_arn):
        container_instances = self._client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=[container_arn]
        )

        instance_ids = []
        for instance in container_instances["containerInstances"]:
            instance_ids.append(instance["ec2InstanceId"])

        instances = self._ec2_client.describe_instances(
            InstanceIds=instance_ids
        )

        result = []
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                result.append(instance)

        return result


def main(args=None):
    parser = ArgumentParser(description="Discover ECS services")
    add_aws_client_arguments(parser)

    parser.add_argument("cluster_name")
    parser.add_argument("container_port")

    args = parser.parse_args(args)

    aws_client = AWSClient("ecs", args)
    ec2_client = AWSClient("ec2", args)
    client = ECSTaskDiscovery(aws_client, ec2_client)
    task_descs = client.find_tasks(args.cluster_name)

    names = []
    for task in task_descs:
        for network_binding in client.find_network_bindings(task, args.container_port, args.cluster_name):
            names.append({
                "{#TASKARN}": task["taskArn"],
                "{#BINDIP}": network_binding[1],
                "{#HOSTPORT}": network_binding[0]["hostPort"]
            })
    discovery = {"data": names}
    print(json.dumps(discovery))


if __name__ == "__main__":
    main()
