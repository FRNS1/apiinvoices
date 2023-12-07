from flask import Flask
from flask_cors import CORS
from .routes.invoices import invoices_bp
from .routes.webhook import webhook_bp
from .routes.services.functionsFile import functions
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta



def create_app():
    app = Flask(__name__)
    scheduler = APScheduler()
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        
    ### Faz o agendamento do Job para enviar invoices a cada 3 horas
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['JOBS'] = [
        {
            'id': 'create_invoice_job',
            'func': functions.sendInvoicesEvery3Hours(),
            'trigger': 'interval',
            'hours': 1,
        }
    ]
    
    scheduler.init_app(app)
    scheduler.start()
    
    ### Faz o primeiro envio das invoices
    functions.sendInvoicesEvery3Hours()
    
    app.register_blueprint(invoices_bp, url_prefix='/invoices')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    return app