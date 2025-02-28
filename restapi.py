
# This was deployed on aws using AWS lambda and API Gateway
import json
from datetime import datetime
import requests
def lambda_handler(event, context):
    
    # TODO implement
    headers: {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    body = event.get('body', '{}')
        
    try:
        # Parsing the JSON body
        body_data = json.loads(body)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }
    try:
        response_id = body_data.get('responseId')
        query_text = body_data.get('queryResult', {}).get('queryText')
        order_id = body_data.get('queryResult', {}).get('parameters', {}).get('order_id')
    
        #order_id = 0
        #order_id = event['queryResult']['parameters']['order_id']
    except KeyError:
        return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "fulfillmentText": order_id
        })
    }
        

    url = "https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus"
    payload = {"orderId": order_id}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        shipment_date = response_data.get('shipmentDate', 'Unknown date')
    except Exception as e:
        return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "fulfillmentText": f"An error occurred while fetching the shipment date: {str(e)}"
        })
    }
        
    shipment_date = datetime.fromisoformat(response_data['shipmentDate'][:-1])

    formatted_date = shipment_date.strftime('%A, %d %b %Y')
    # Prepare the response to be sent back to DialogFlow
    fulfillment_text = f"The shipment date for your order {order_id} is {formatted_date}."
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
        "fulfillmentText": fulfillment_text
    })
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
