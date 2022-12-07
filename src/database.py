from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


payment_invoice_m2m = db.Table(
    "payment_invoice",
    db.Column("payment_id", db.ForeignKey('payment.id'), primary_key=True),
    db.Column("invoice_id", db.ForeignKey('invoice.id'), primary_key=True),
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), unique=False, nullable=False)
    last_name = db.Column(db.String(64), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
    invoices = db.relationship("Invoice", backref="customer")
    payments = db.relationship("Payment", backref="customer")

    def __repr__(self) -> str:
        return f"Customer id: {self.id} >>> Customer name: {self.first_name} {self.last_name}"


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    amount = db.Column(db.Float, default=0.0)
    remaining_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())


    def __repr__(self) -> str:
        return f"Invoice #>> {self.id} asigned to a customer with id {self.customer_id}"



class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    #the invoices that the customers pays
    invoices = db.relationship("Invoice", secondary=payment_invoice_m2m, backref="payments")
    

    def __repr__(self) -> str:
        return f"Payment #>> {self.id} asigned to {self.customer_id}"



