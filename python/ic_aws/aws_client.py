#!/usr/bin/python

import boto3


class AWSClient(object):
    """AWS API client class."""

    def __init__(self, service, args):
        """Initializes connection to AWS service using boto3 client."""
        self._client = boto3.client(
            service,
            region_name=args.region_name,
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key)

    def client(self):
        return self._client


def add_aws_client_arguments(parser):
    """Adds command line options for AWS client to argparse parser."""
    parser.add_argument("-r", "--region", dest="region_name")
    parser.add_argument("-k", "--access-key-id", dest="aws_access_key_id")
    parser.add_argument("-s", "--secret-access-key",
                        dest="aws_secret_access_key")


if __name__ == "__main__":
    pass
