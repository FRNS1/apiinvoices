from flask import Blueprint, jsonify, make_response
from .services.functionsFile import functions

invoices_bp = Blueprint('invoices', __name__)

### Endpoint para chamada de função que cria os invoices
@invoices_bp.route('/createinvoice', methods=['GET'])
def createInvoice():
    invoice = functions.sendInvoicesEvery3Hours()
    return make_response(
        jsonify(
            mensagem='ok',
            dados=invoice
        ), 200
    )