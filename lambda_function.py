import json
import requests

### Função rodando no AWS Lambdas que recebe a chamada do webhook
### Endereço da função: https://5wfrcbsfian7vzptzzbvn6rx5q0cfwts.lambda-url.sa-east-1.on.aws/

def lambda_handler(event, context):

    if 'body' in event:
        invoice = json.dumps(event['body'])
        url = "http://52.67.209.166:5000/webhook/getinvoice"
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=invoice)
        return response.text
    else:
        return "Invoice não está presente!"