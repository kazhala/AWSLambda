import boto3
from botocore.exceptions import ClientError

regions = ['ap-southeast-2']


def lambda_handler(event, context):
    for region in regions:
        client = boto3.client('cloudformation', region_name=region)
        paginator = client.get_paginator('describe_stacks')
        for result in paginator.paginate():
            for stack in result.get('Stacks', []):
                stack_name = stack.get('StackName')
                stack_status = stack.get(
                    'DriftInformation').get('StackDriftStatus')
                print('Region: %s  StackName: %s  Status: %s' %
                      (region, stack_name, stack_status))
                try:
                    client.detect_stack_drift(StackName=stack_name)
                except ClientError as e:
                    print(e)
