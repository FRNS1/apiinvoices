
Sobre a implementação da aplicação, desenvolvi uma API em Python utilizando o framework Flask e a hospedei em uma instância AWS EC2 (IP público: 52.67.209.166). Utilizei o Flask Scheduler para agendar uma tarefa ao iniciar a aplicação e, subsequentemente, a cada 180 minutos (3 horas). Além disso, criei um endpoint (/invoices/createinvoice) com a mesma funcionalidade, caso haja a necessidade de acionar a função manualmente. Este endpoint gera de 8 a 12 invoices a cada intervalo de 3 horas.

No que diz respeito à detecção de pagamentos, desenvolvi uma função serverless (lambda_function.py) e a hospedei em uma instância AWS Lambda (URL da função: https://5wfrcbsfian7vzptzzbvn6rx5q0cfwts.lambda-url.sa-east-1.on.aws/). Esta solução resolve o problema anterior relacionado ao cadastro do webhook. A função recebe dados enviados pelo Stark Bank e os encaminha para a minha API. Na API, são realizadas duas validações: uma de status e outra de externalId (concatenação da palavra 'external' com o ID da invoice paga, por exemplo: external-8374837834). Ao iniciar a API, é chamada uma função que retorna todas as transferências realizadas até o momento. O externalId de cada transferência é armazenado em uma lista. Portanto, a função que realiza a transferência só é invocada se o status for 'paid' e o externalId não estiver na lista de transferências existentes, garantindo a ausência de transferências duplicadas. Após a conclusão, o externalId da nova transferência é adicionado à lista.

Endpoints:

Invoices: http://52.67.209.166:5000/invoices/createinvoice
Transferências: http://52.67.209.166:5000/webhook/getinvoice
URL Lambdas: https://5wfrcbsfian7vzptzzbvn6rx5q0cfwts.lambda-url.sa-east-1.on.aws/
Repositório: https://github.com/FRNS1/apiinvoices.git
Observação: A minha privateKey foi deixada no repositório porque não tinha certeza se vocês a corrigiriam usando ela ou uma própria. Estou ciente de que devo adicionar o arquivo ao .gitignore.
