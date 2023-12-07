from flask import Blueprint, jsonify, make_response, request
from .services.functionsFile import functions
import json

webhook_bp = Blueprint('webhook', __name__)

### Pega todas as transferências existentes, isso ajuda a não enviar transferências duplicadas
listTransfers = []
transfers = functions.getAllTransfers()
for transfer in transfers['transfers']:
    listTransfers.append(transfer['externalId'])

### Endpoint responsável pela realização de transferências chamado pela função serverless que é acionada pelo webhook
@webhook_bp.route('/getinvoice', methods=['POST'])
def hookReceiver():
    data = request.get_json()
    jsonData = json.loads(data)
    if data:
        amount = jsonData['event']['log']['invoice']['amount']
        status = jsonData['event']['log']['invoice']['status']
        externalId = f"external-{jsonData['event']['log']['invoice']['id']}"
        if status == 'paid' and externalId not in listTransfers:
            transfer = functions.transfer(amount, externalId)
            listTransfers.append(transfer['transfers'][0]['externalId'])
            return make_response(
                jsonify(
                    mensagem='Ok',
                    data=transfer
                ), 200
            )
        else:
            return make_response(
            jsonify(
                mensagem='Não paga',
            ), 200
            )
    else:
        return make_response(
            jsonify(
                mensagem='falha',
            ), 200
        )