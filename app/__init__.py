from flask import Flask
from flask_cors import CORS
from .routes.invoices import invoices_bp
from .routes.webhook import webhook_bp
from .routes.services.functionsFile import functions
from flask_apscheduler import APScheduler

def create_app():
    app = Flask(__name__)
    scheduler = APScheduler()
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    def createInvoiceJob():
        invoice = functions.sendInvoicesEvery3Hours()
        print("Job executed:", invoice)
        
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['JOBS'] = [
        {
            'id': 'create_invoice_job',
            'func': createInvoiceJob,
            'trigger': 'interval',
            'hours': 3,
        }
    ]
    
    scheduler.init_app(app)
    scheduler.start()
    
    app.register_blueprint(invoices_bp, url_prefix='/invoices')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    return app