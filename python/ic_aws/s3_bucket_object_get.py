#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from ic_aws.aws_client import AWSResourceClient, add_aws_client_arguments


class S3BucketObjectGet(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()

    def s3_bucket_object_get(self, bucket_name, object_key, encoding):
        """Get object contents from S3 bucket."""

        obj = self._client.Object(bucket_name, object_key)
        return obj.get()['Body'].read().decode(encoding)


def main(args=None):
    parser = ArgumentParser(description="Get S3 bucket object contents")
    add_aws_client_arguments(parser)

    parser.add_argument("bucket_name", help="S3 bucket name")
    parser.add_argument("object_key", help="S3 object key")
    parser.add_argument("encoding", default="utf-8", help="Object encoding")

    args = parser.parse_args(args)

    aws_client = AWSResourceClient("s3", args)
    client = S3BucketObjectGet(aws_client)
    contents = client.s3_bucket_object_get(args.bucket_name, args.object_key, args.encoding)
    print(contents)


if __name__ == "__main__":
    main()
