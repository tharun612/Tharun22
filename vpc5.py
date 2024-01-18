import boto3
import time

# Set up DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'pranav1'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)

# Set up EC2 resource
ec2 = boto3.resource('ec2', region_name='ap-south-1')

def fetch_available_cidr_and_create_vpc():
    # Query the DynamoDB table for an item with 'Status' equal to 'Available'
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('Status').eq('Available')
    )

    # Get the first available item
    item = response.get('Items', [])[0] if response.get('Items') else None

    if item:
        # Extract CIDR from the DynamoDB item
        cidr_range = item.get('CIDR')

        # Update DynamoDB item status to 'In-Progress'
        update_dynamodb_status(item['Sr.NO'], 'In-Progress')

        # Introduce a delay (e.g., 10 seconds) before creating the VPC
        time.sleep(20)

        # Create VPC
        vpc = ec2.create_vpc(CidrBlock=cidr_range)

        # Introduce another delay (e.g., 5 seconds) before updating the status to 'In-Use'
        time.sleep(10)

        # Update DynamoDB item status to 'In-Use' after successful creation
        update_dynamodb_status(item['Sr.NO'], 'In-Use')

        print(f"VPC created with CIDR: {cidr_range}")
    else:
        print("No available CIDR found in the DynamoDB table.")

def update_dynamodb_status(sr_no, new_status):
    # Update DynamoDB item status based on 'Sr.NO'
    table.update_item(
        Key={'Sr.NO': sr_no},
        UpdateExpression="SET #status = :new_status",
        ExpressionAttributeNames={'#status': 'Status'},
        ExpressionAttributeValues={':new_status': new_status},
        ReturnValues="UPDATED_NEW"
    )

if __name__ == "__main__":
    fetch_available_cidr_and_create_vpc()

