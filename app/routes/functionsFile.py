import time
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.ecdsa import Ecdsa
import requests
import json
import random

class functions:

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
        privateKey = PrivateKey.fromPem("""
        -----BEGIN EC PARAMETERS-----
        BgUrgQQACg==
        -----END EC PARAMETERS-----
        -----BEGIN EC PRIVATE KEY-----
        MHQCAQEEIIeTDvpQgt230UWY6dxB7JTLhQ91nI7/BL1CySP0ZKLWoAcGBSuBBAAK
        oUQDQgAELpc8LwSIOOjzoL+iSO7ok8VB7mrsw5/B/XPsE2pxt2n3DgVFGitNHIu7
        k9Ge1IzE/mY87uGWYRpd4P6YwfCvRw==
        -----END EC PRIVATE KEY-----
        """)
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

    def getInvoice(id):
        accessTime = int(time.time())
        accessId = "project/6227762025070592"
        bodyString = ""
        message = f"{accessId}:{accessTime}:{bodyString}"
        privateKey = PrivateKey.fromPem("""
        -----BEGIN EC PARAMETERS-----
        BgUrgQQACg==
        -----END EC PARAMETERS-----
        -----BEGIN EC PRIVATE KEY-----
        MHQCAQEEIIeTDvpQgt230UWY6dxB7JTLhQ91nI7/BL1CySP0ZKLWoAcGBSuBBAAK
        oUQDQgAELpc8LwSIOOjzoL+iSO7ok8VB7mrsw5/B/XPsE2pxt2n3DgVFGitNHIu7
        k9Ge1IzE/mY87uGWYRpd4P6YwfCvRw==
        -----END EC PRIVATE KEY-----
        """)
        signature = Ecdsa.sign(message, privateKey)
        accessSignature = signature.toBase64()

        request = requests.get(
            url=f"https://sandbox.api.starkbank.com/v2/invoice/{id}",
            headers={
                "Access-Id" : accessId,
                "Access-Time" : f"{accessTime}",
                "Access-Signature": accessSignature
            }
        )

        return json.loads(request.text)

    def transfer(amount):
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
                "accountType": "payment"
                }]
        }
        bodyStringJSON = json.dumps(bodyString)
        message = f"{accessId}:{accessTime}:{bodyStringJSON}"
        privateKey = PrivateKey.fromPem("""
        -----BEGIN EC PARAMETERS-----
        BgUrgQQACg==
        -----END EC PARAMETERS-----
        -----BEGIN EC PRIVATE KEY-----
        MHQCAQEEIIeTDvpQgt230UWY6dxB7JTLhQ91nI7/BL1CySP0ZKLWoAcGBSuBBAAK
        oUQDQgAELpc8LwSIOOjzoL+iSO7ok8VB7mrsw5/B/XPsE2pxt2n3DgVFGitNHIu7
        k9Ge1IzE/mY87uGWYRpd4P6YwfCvRw==
        -----END EC PRIVATE KEY-----
        """)
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

    def randomPerson():
        api_url = 'https://api.api-ninjas.com/v1/randomuser'
        request = requests.get(api_url, headers={'X-Api-Key': 'UFrsF924j4T5U8/vbVTJdg==wVhAoX9cDFejrRvw'})
        return json.loads(request.text)

    def gerarCpf():
        cpfNumeros = [random.randint(0, 9) for _ in range(9)]
        soma = sum((i + 1) * num for i, num in enumerate(cpfNumeros))
        primeiroDigito = (soma % 11) % 10
        cpfNumeros.append(primeiroDigito)
        soma = sum((i + 1) * num for i, num in enumerate(cpfNumeros))
        segundo_digito = (soma % 11) % 10
        cpfNumeros.append(segundo_digito)
        cpf = ''.join(map(str, cpfNumeros))
        return cpf

    def sendInvoicesEvery3Hours():
        randomNumber = random.randint(8, 12)
        invoicesList = []
        for i in range(randomNumber):
            person = functions.randomPerson()
            cpf = functions.gerarCpf()
            randomAmount= random.randrange(1, 10)
            invoice = functions.createInvoice(randomAmount, cpf, person['name'])
            print(invoice)
            invoicesList.append(invoice['invoices'][0]['id'])
        return invoicesList

        