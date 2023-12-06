from flask import Blueprint, jsonify, make_response, request
from .services.functionsFile import functions

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/getinvoice', methods=['POST'])
def hookReceiver():
    data = request.get_json()
    if data:
        print('------------------------------------')
        print(data)
        print('------------------------------------')
        transfer = functions.transfer(data['amount'])
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
                mensagem='falha',
            ), 200
        )