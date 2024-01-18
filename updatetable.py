import boto3

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
table = dynamodb.Table('pranav1')

response = table.update_item(
        Key={'Sr.NO': 1},
    UpdateExpression="SET #s = :s",
    ExpressionAttributeNames={'#s': 'Status'},
    ExpressionAttributeValues={':s': 'In-Use'},
    ReturnValues="UPDATED_NEW"
)

print(response['Attributes'])

