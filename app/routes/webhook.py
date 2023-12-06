from flask import Blueprint, jsonify, make_response, request
from .services.functionsFile import functions
import json

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/getinvoice', methods=['POST'])
def hookReceiver():
    data = request.get_json()
    jsonData = json.loads(data)
    if data:
        print('------------------------------------')
        print(jsonData)
        print('------------------------------------')
        amount = jsonData['event']['log']['invoice']['amount']
        status = jsonData['event']['log']['invoice']['status']
        if status == 'paid':
            transfer = functions.transfer(amount)
            print('------------------------------------')
            print(transfer)
            print('------------------------------------')
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