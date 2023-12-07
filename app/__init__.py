from flask import Flask
from flask_cors import CORS
from app.routes.invoices import invoices_bp
from app.routes.webhook import webhook_bp
from .routes.services.functionsFile import functions
from flask_apscheduler import APScheduler

def create_app():
    app = Flask(__name__)
    scheduler = APScheduler()
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    ### Função para ser usada no scheduler
    def sendInvoices():
        invoices = functions.sendInvoicesEvery3Hours()
        
    ### Faz o agendamento do Job para enviar invoices a cada 3 horas
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['JOBS'] = [
        {
            'id': 'create_invoice_job',
            'func': sendInvoices,
            'trigger': 'interval',
            'minutes': 5,
        }
    ]
    
    scheduler.init_app(app)
    scheduler.start()
    
    ### Faz o primeiro envio das invoices
    functions.sendInvoicesEvery3Hours()
    
    app.register_blueprint(invoices_bp, url_prefix='/invoices')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    return app