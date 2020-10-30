#!/usr/bin/python3

from argparse import ArgumentParser
from aws_client import AWSClient, add_aws_client_arguments
import json


class RDSDiscovery(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()

    def find_cluster_members(self, cluster_identifier):
        clusters = self._client.describe_db_clusters(
            DBClusterIdentifier=cluster_identifier
        )

        if len(clusters["DBClusters"]) > 0:
            cluster = clusters["DBClusters"][0]
            return cluster["DBClusterMembers"]
        else:
            return []


def main(args=None):
    parser = ArgumentParser(description="Discover RDS services")
    add_aws_client_arguments(parser)

    parser.add_argument("cluster_identifier")

    args = parser.parse_args(args)

    aws_client = AWSClient("rds", args)
    client = RDSDiscovery(aws_client)
    members = client.find_cluster_members(args.cluster_identifier)

    identifiers = []
    for member in members:
        identifiers.append({
                "{#DB_IDENTIFIER}": member["DBInstanceIdentifier"]
            })
    discovery = {"data": identifiers}
    print(json.dumps(discovery))


if __name__ == "__main__":
    main()
