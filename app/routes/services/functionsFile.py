import time
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.ecdsa import Ecdsa
from config import privateKey as pkey
import requests
import json
import random

class functions:
    
    ### Requisição no sandbox do Stark Bank para listar todas transferências
    def getAllTransfers():
        accessTime = int(time.time())
        accessId = "project/6227762025070592"
        bodyString = ""
        message = f"{accessId}:{accessTime}:{bodyString}"
        privateKey = PrivateKey.fromPem(pkey)
        signature = Ecdsa.sign(message, privateKey)
        accessSignature = signature.toBase64()
        request = requests.get(
        url=f"https://sandbox.api.starkbank.com/v2/transfer",
        headers={
            "Access-Id" : accessId,
            "Access-Time" : f"{accessTime}",
            "Access-Signature": accessSignature
            }
        )

        return json.loads(request.text)

    ### Requisição no sandbox do Stark Bank para criar uma invoice
    def createInvoice(amount, taxId, name):
        accessTime = int(time.time())
        accessId = "project/6227762025070592"
        bodyString = {
            "invoices":[{
                "amount": amount,
                "taxId": f"{taxId}",
                "name": f"{name}"
                }]
        }
        bodyStringJSON = json.dumps(bodyString)
        message = f"{accessId}:{accessTime}:{bodyStringJSON}"
        privateKey = PrivateKey.fromPem(pkey)
        signature = Ecdsa.sign(message, privateKey)
        accessSignature = signature.toBase64()
        request = requests.post(
            url="https://sandbox.api.starkbank.com/v2/invoice",
            data=json.dumps(bodyString),
            headers={
                "Access-Id" : accessId,
                "Access-Time" : f"{accessTime}",
                "Access-Signature": accessSignature
            }
        )

        return json.loads(request.text)

    ### Requisição no sandbox do Stark Bank para criar uma transferência
    def transfer(amount, externalId):
        accessTime = int(time.time())
        accessId = "project/6227762025070592"
        bodyString = {
            "transfers":[{
                "amount": amount,
                "name": "Stark Bank S.A.",
                "taxId": "20.018.183/0001-80",
                "bankCode": "20018183",
                "branchCode": "0001",
                "accountNumber": "6341320293482496",
                "accountType": "payment",
                "externalId": externalId
                }]
        }
        bodyStringJSON = json.dumps(bodyString)
        message = f"{accessId}:{accessTime}:{bodyStringJSON}"
        privateKey = PrivateKey.fromPem(pkey)
        signature = Ecdsa.sign(message, privateKey)
        accessSignature = signature.toBase64()
        request = requests.post(
        url=f"https://sandbox.api.starkbank.com/v2/transfer",
        data=bodyStringJSON,
        headers={
            "Access-Id" : accessId,
            "Access-Time" : f"{accessTime}",
            "Access-Signature": accessSignature
            }
        )

        return json.loads(request.text)

    ### Requisição na api-ninjas para conseguir nomes aleatórios
    def randomPerson():
        api_url = 'https://api.api-ninjas.com/v1/randomuser'
        request = requests.get(api_url, headers={'X-Api-Key': 'UFrsF924j4T5U8/vbVTJdg==wVhAoX9cDFejrRvw'})
        return json.loads(request.text)

    ### Função usada para gerar um CPF aleatório válido
    def gerarCpf():
        while True:
            cpf = [random.randint(0, 9) for i in range(9)]
            if cpf != cpf[::-1]:
                break
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            cpf.append(digit)
        result = ''.join(map(str, cpf))
        return result
    
    ### Função que faz o envio das invoices 
    def sendInvoicesEvery3Hours():
        randomNumber = random.randint(8, 12)
        invoicesList = []
        for i in range(randomNumber):
            person = functions.randomPerson()
            cpf = functions.gerarCpf()
            randomAmount = random.randint(1, 1000)
            invoice = functions.createInvoice(randomAmount, cpf, person['name'])
            try:
                invoicesList.append(invoice['invoices'][0]['id'])
            except:
                return invoice
        return invoicesList

        