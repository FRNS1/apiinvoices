from flask import Blueprint, jsonify, make_response

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/getinvoice', methods=['POST'])
def hookReceiver():
    return make_response(
        jsonify(
            mensagem='Ok'
        ), 200
    )