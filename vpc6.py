import boto3
import time


dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'pranav1'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)


ec2 = boto3.resource('ec2', region_name='ap-south-1')

def fetch_available_cidr_and_create_vpc():

    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('Status').eq('Available')
    )

    
    item = response.get('Items', [])[0] if response.get('Items') else None

    if item:
        
        cidr_range = item.get('CIDR')

        try:
            # Update DynamoDB item status to 'In-Progress'
            update_dynamodb_status(item['Sr.NO'], 'In-Progress')

        
            time.sleep(15)

            # Create VPC
            vpc = ec2.create_vpc(CidrBlock=cidr_range)

        
            time.sleep(10)

        
            update_dynamodb_status(item['Sr.NO'], 'In-Use')

            print(f"VPC created with CIDR: {cidr_range}")
        except Exception as e:
            # If VPC creation fails, update status back to 'Available'
            print(f"VPC creation failed with error: {str(e)}")
            update_dynamodb_status(item['Sr.NO'], 'Available')
    else:
        print("No available CIDR found in the DynamoDB table.")

def update_dynamodb_status(sr_no, new_status):
    
    table.update_item(
        Key={'Sr.NO': sr_no},
        UpdateExpression="SET #status = :new_status",
        ExpressionAttributeNames={'#status': 'Status'},
        ExpressionAttributeValues={':new_status': new_status},
        ReturnValues="UPDATED_NEW"
    )

if __name__ == "__main__":
    fetch_available_cidr_and_create_vpc()

