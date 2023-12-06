from marshmallow import Schema, fields

class invoiceSchema(Schema):
    amount = fields.String()