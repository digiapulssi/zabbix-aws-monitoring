#!/usr/bin/python3

from argparse import ArgumentParser
from aws_client import AWSClient, add_aws_client_arguments
import json


class LambdaDiscovery(object):
    def __init__(self, aws_client):
        self._client = aws_client.client()
        
    def get_functions(self, pagination_token=None):
        
        if pagination_token:
            result = self._client.list_functions(Marker=pagination_token)
        else:
            result = self._client.list_functions()

        return result
    
    
def main(args=None):
    parser = ArgumentParser(description="Discover Lambda functions")
    add_aws_client_arguments(parser)
    
    args = parser.parse_args(args)
    
    aws_client = AWSClient("lambda", args)
    client = LambdaDiscovery(aws_client)
    
    result = client.get_functions()
    functions = result['Functions']

    # Max function return count is 50
    # if n(functions)>50 pagnation token "NextMarker" will be returned
    while 'NextMarker' in result:
        result = client.get_functions(pagination_token = result['NextMarker'])
        functions.extend(result['Functions'])

    discover_functions = []
    for function in functions:
        discover_functions.append({'{#FUNCTIONNAME}': function['FunctionName'],
                                   '{#DESCRIPTION}': function['Description']})
        
    discovery = {'data': discover_functions}
    print(json.dumps(discovery))
    
if __name__ == "__main__":
    main()
