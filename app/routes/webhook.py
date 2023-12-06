from flask import Blueprint, jsonify, make_response, request
from .services.functionsFile import functions
import json

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/getinvoice', methods=['POST'])
def hookReceiver():
    data = request.get_json()
    data = json.dumps(data)
    if data:
        print('------------------------------------')
        print(data)
        print('------------------------------------')
        print(type(data))
        print('------------------------------------')
        amount = data['event']['log']['invoice']['amount']
        status = data['event']['log']['invoice']['status']
        if status == 'paid':
            transfer = functions.transfer(amount)
            print(transfer)
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