import boto3
 
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'pranav1'  
table = dynamodb.Table(table_name)
 
# Set up EC2 resource
ec2 = boto3.resource('ec2', region_name='ap-south-1')
 
def fetch_available_cidr_and_create_vpc():
    
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('Status').eq('Available')
    )
 
   
    item = response.get('Items', [])[0] if response.get('Items') else None
 
    if item:
        
        cidr_range = item.get('CIDR')
 
        
        vpc = ec2.create_vpc(CidrBlock=cidr_range)
 
        # Update DynamoDB item status to 'In-Use'
        update_dynamodb_status(item['Sr.NO'], 'In-Use')
 
        print(f"VPC created with CIDR: {cidr_range}")
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
