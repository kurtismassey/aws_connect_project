import boto3 
import os
import requests
import json
   
def postcode_api_lookup(event, context):
    contact_number = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
    postal_code = event["Details"]["Parameters"]["PostalCode"]

    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    try:
        lookup_response = requests.get(f"https://api.postcodes.io/postcodes/{postal_code}")
        lookup_response = lookup_response.json()
        print("Postcode Look Up Complete")
    except: 
        print("Lookup Failed")

    local_authority = lookup_response["result"]["admin_district"]

    response = table.put_item(Item={
        "contact_number": contact_number,
        "location": local_authority
    })
    
    local_authority_result = { 
        "LocalAuthority": local_authority
    }
    
    return local_authority_result

# For Local Testing

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "test_lookup"
    event = { "Details": { 
        "ContactData": {
            "CustomerEndpoint": { 
                "Address" : "+445453453534"
                }
            },
        "Parameters": {
            "PostalCode": "LS1 3AD"
        }
        } 
    }
    print(postcode_api_lookup(event, None))