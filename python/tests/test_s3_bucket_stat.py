#!/usr/bin/python

import sys
import os
import unittest
from mock import Mock, call, patch
from dateutil.tz import tzlocal
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ic_aws.s3_bucket_stat import S3BucketStat  # noqa


class MockAWSClient:
    def __init__(self):
        self._client = Mock()

    def client(self):
        return self._client


class TestS3BucketStat(unittest.TestCase):

    d1 = datetime(2018, 1, 1, 0, 0, 0, 0, tzlocal())
    d2 = datetime(2018, 2, 1, 0, 0, 0, 0, tzlocal())
    now = datetime(2018, 3, 1, 0, 0, 0, 0, tzlocal())

    bucket_list = {
        "IsTruncated": False,
        "Contents": [
            {
                "LastModified": d1,
                "Size": 10000
            },
            {
                "LastModified": d2,
                "Size": 10000
            }
        ]
    }

    def stable_now(self):
        return TestS3BucketStat.now

    @patch.object(S3BucketStat, "now_with_tz", stable_now)
    def test_bucket_oldest(self):
        aws_client = MockAWSClient()
        aws_client.client().list_objects_v2.return_value = self.bucket_list

        sut = S3BucketStat(aws_client)
        result = sut.s3_bucket_stat("test", "oldest")
        self.assertEqual((self.stable_now() - self.d1).total_seconds(), result)

    @patch.object(S3BucketStat, "now_with_tz", stable_now)
    def test_bucket_newest(self):
        aws_client = MockAWSClient()
        aws_client.client().list_objects_v2.return_value = self.bucket_list

        sut = S3BucketStat(aws_client)
        result = sut.s3_bucket_stat("test", "newest")
        self.assertEqual((self.stable_now() - self.d2).total_seconds(), result)

    def test_bucket_oldest(self):
        aws_client = MockAWSClient()
        aws_client.client().list_objects_v2.return_value = self.bucket_list

        sut = S3BucketStat(aws_client)
        result = sut.s3_bucket_stat("test", "size")
        self.assertEqual(20000, result)
