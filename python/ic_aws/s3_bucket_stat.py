#!/usr/bin/python

import sys
from dateutil.tz import tzlocal
from datetime import datetime
from argparse import ArgumentParser
from aws_client import AWSClient, add_aws_client_arguments


class MinValueVisitor(object):
    """Visitor that searches field with minimum value."""

    def __init__(self, field):
        self.min = None
        self.field = field

    def visit(self, item):
        if self.min is None:
            self.min = item
        elif self.min[self.field] > item[self.field]:
            self.min = item

    def value(self):
        if self.min is not None:
            return self.min[self.field]
        else:
            return None


class MaxValueVisitor(object):
    """Visitor that searches field with maximum value."""

    def __init__(self, field):
        self.max = None
        self.field = field

    def visit(self, item):
        if self.max is None:
            self.max = item
        elif self.max[self.field] < item[self.field]:
            self.max = item

    def value(self):
        if self.max is not None:
            return self.max[self.field]
        else:
            return None


class SumVisitor(object):
    """Visitor that calculates sum from field values."""

    def __init__(self, field):
        self.total = 0
        self.field = field

    def visit(self, item):
        self.total = self.total + item[self.field]

    def value(self):
        return self.total


class S3BucketStat(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()

    def iterate_bucket(self, bucket_name, visitor):
        """Iterates through S3 bucket and calls supplied visitor for each
        object."""

        # Request object list from bucket
        response = self._client.list_objects_v2(
            Bucket=bucket_name
        )

        # Visit each item in response contents
        for item in response["Contents"]:
            visitor.visit(item)

        while response["IsTruncated"]:
            cont_token = response["NextContinuationToken"]

            # Request object list continutation from bucket
            response = self._client.list_objects_v2(
                Bucket=bucket_name,
                ContinuationToken=cont_token
            )

            # Visit each item in response contents
            for item in response["Contents"]:
                visitor.visit(item)

    def now_with_tz(self):
        return datetime.now(tzlocal())

    def s3_bucket_stat(self, bucket_name, stat):
        """Retrieves named statistic from S3 bucket."""

        if stat == "oldest":
            visitor = MinValueVisitor("LastModified")
            self.iterate_bucket(bucket_name, visitor)
            return (self.now_with_tz() - visitor.value()).total_seconds()
        elif stat == "newest":
            visitor = MaxValueVisitor("LastModified")
            self.iterate_bucket(bucket_name, visitor)
            return (self.now_with_tz() - visitor.value()).total_seconds()
        elif stat == "size":
            visitor = SumVisitor("Size")
            self.iterate_bucket(bucket_name, visitor)
            return visitor.value()
        else:
            print "Invalid stat name {}.".format(stat)
            sys.exit(1)


def main(args=None):
    parser = ArgumentParser(description="Calculate statistics of S3 bucket")
    add_aws_client_arguments(parser)

    available_stats = ["oldest", "newest", "size"]
    parser.add_argument("bucket_name", help="S3 bucket name")
    parser.add_argument("stat", help="Statistic to calculate",
                        choices=available_stats)

    args = parser.parse_args(args)

    aws_client = AWSClient("s3", args)
    client = S3BucketStat(aws_client)
    value = client.s3_bucket_stat(args.bucket_name, args.stat)
    if value == -1:
        print("")
    else:
        print(value)


if __name__ == "__main__":
    main()
