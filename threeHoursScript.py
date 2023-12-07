import time
import requests

### Essa é uma segunda opção para chamar o endpoint da API que cria invoices a cada 3 horas
def requestApi():
    url = "http://52.67.209.166:5000/invoices/createinvoice"
    response = requests.get(url)
    return response

intervaloCriarInvoices = 3 * 60 * 60
ultimaExecucaoCriarInvoices = time.time()

try:
    requestApi()
    while True:
        currentTime = time.time()
        if currentTime - ultimaExecucaoCriarInvoices >= intervaloCriarInvoices:
            requestApi()
            ultimaExecucaoCriarInvoices = currentTime      
        time.sleep(10)
except KeyboardInterrupt:
    print("Script interrompido pelo usuário.")



