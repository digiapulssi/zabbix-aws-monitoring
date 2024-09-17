#!/usr/bin/env python

# Python imports
from argparse import ArgumentParser
import json
import re

# Script imports
from ic_aws.aws_client import AWSClient, add_aws_client_arguments


class FunctionCaller(object):

    '''Calls a specified function in boto3 library with given arguments'''

    def __init__(self, aws_client, function_name, arguments=None):
        self._client = aws_client.client()
        self.arguments = self.parse_arguments(arguments)
        self.function = self.get_function(function_name)


    def parse_arguments(self, arguments):
        if(arguments):
            output = {}

            # Parse arguments (key-value pairs). Arguments can be given in two forms:
            # String form: key1=value1,key2=value2,key3=value3
            # List form  : key1=/1,2,3/,key2=/4,5,6/,key3=/7,8,9/
            # Forward slashes are used instead of brackets because brackets are not allowed in
            # Zabbix UserParameter keys.
            while len(arguments) > 0:

                # Extract a key-value pair from the beginning of arguments
                match = re.match(r"([-\w]+)=(/[-,\w]+/|[-\w]+)(?:,|$)", arguments)

                # Check for match before proceeding
                if not match:
                    raise ValueError("Error while matching query arguments.")

                # Grab key and value from RegEx matched tuple
                key, value = match[1], match[2]

                # Remove matched key-value pair from arguments
                arguments = arguments[len(match[0]):]

                # Convert "list formatted" string to Python list, e.g. /1,2,3/ -> [1, 2, 3]
                if value[0] == "/" and value[-1] == "/":
                    value = value[1:-1].split(",")

                # Add key-value pair to dictionary
                output[key] = value

            return output

    def get_function(self, function_name):

        return getattr(self._client, function_name)

    def get_results(self):

        if self.arguments:
            return self.function(**self.arguments)
        else:
            return self.function()


# Used for unserializable fields like date
def unserializable_to_str(item):
    return item.__str__()

def main(args=None):

    parser = ArgumentParser(description="")

    # Create aws client and parse arguments
    add_aws_client_arguments(parser)
    parser.add_argument("-n", "--namespace", help="Namespace of AWS service")
    parser.add_argument("-f", "--function_name", help="Function that is to be called in boto3 library")
    parser.add_argument("-a", "--arguments",
        help="Arguments that are given to the function. Arguments can be given in two forms. " +
             "String form: key1=value1,key2=value2,key3=value3 " +
             "List form: key1=/1,2,3/,key2=/4,5,6/,key3=/7,8,9/"
    )
    args = parser.parse_args(args)

    # Create aws connection and call specified function
    aws_client = AWSClient(args.namespace, args)
    caller = FunctionCaller(aws_client, args.function_name, args.arguments)
    result = caller.get_results()

    print(json.dumps(result, default = unserializable_to_str))

if __name__ == "__main__":
    main()
