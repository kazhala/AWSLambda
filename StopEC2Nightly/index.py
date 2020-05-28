import boto3


def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print("Region:", region)
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            tags = instance.tags
            is_server = False
            for tag in tags:
                if (tag['Key'] == 'WebServer'):
                    is_server = True
            if not is_server:
                instance.stop()
                print(f"{instance.id} stopped")
            else:
                print(f"{instance.id} is a server")
