import random
from src.database import Invoice


def dump_data(customer_id=1):

    invoices = []

    for _ in range(1, 100):
        amount = round(random.uniform(1.0, 999_999.99), 2)
        invoice = Invoice(
            customer_id=customer_id, amount=amount, remaining_balance=amount
        )
        invoices.append(invoice)

    return invoices
