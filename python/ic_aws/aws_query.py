#!/usr/bin/python3

from argparse import ArgumentParser
from ic_aws.aws_client import AWSClient, add_aws_client_arguments
import json


class FunctionCaller(object):

    def __init__(self, aws_client, function_name, arguments=None):
        self._client = aws_client.client()
        self.arguments = self.parse_arguments(arguments)
        self.function = self.get_function(function_name)
    
        
    def parse_arguments(self, arguments):
        if(arguments):
            return (dict(item.split("=") for item in arguments.split(",")))
    
    def get_function(self, function_name):
        
        return getattr(self._client, function_name)
        
    def get_results(self):
        
        if self.arguments:
            return self.function(**self.arguments)
        else:
            return self.function()

def unserializable_to_str(item):
    return item.__str__()

def main(args=None):
    
    parser = ArgumentParser(description="")
    add_aws_client_arguments(parser)
    
    parser.add_argument("-n", "--namespace")    
    parser.add_argument("-f", "--function_name")
    parser.add_argument("-a", "--arguments")
    args = parser.parse_args(args) 
    
    aws_client = AWSClient(args.namespace, args)
    client = FunctionCaller(aws_client, args.function_name, args.arguments)
    result = client.get_results()
    
    print(json.dumps(result, default = unserializable_to_str))

if __name__ == "__main__":
    main()
