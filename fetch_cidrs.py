# fetch_cidrs.py

import boto3

def fetch_cidrs():
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('pranav1')

    response = table.scan()
    cidrs = [item['CIDR'] for item in response['Items'] if item['Status'] == 'Available']

    print('\n'.join(cidrs))

if __name__ == "__main__":
    fetch_cidrs()

