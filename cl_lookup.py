import boto3 
import os
   
def client_lookup(event, context):
    contact_number = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]

    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={"contact_number": contact_number})

    if "Item" in response: 
        client_location = response["Item"]["location"]
        message = f"It looks like you've used this service before, are you still based in {client_location}?"
        repeat_caller = 1
        print("Client found, returning location response")
    else:
        message = "In order to connect you to your local service we need to collect some details, please say yes if you're happy to proceed"
        repeat_caller = 0
        print("Client not found, returning first time response")
    
    lookup_results = { 
        "Message": message, 
        "RepeatCaller": repeat_caller
    }
    
    return lookup_results

# For Local Testing

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "test_lookup"
    event = { "Details": { 
        "ContactData": {
            "CustomerEndpoint": { 
                "Address" : "+445453453534"
                }
            } 
        } 
    }
    print(client_lookup(event, None))