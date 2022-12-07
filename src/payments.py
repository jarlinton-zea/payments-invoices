from src.constants.http_status_codes import *
from flask import Blueprint, request, jsonify
from src.database import Payment, Invoice, db
from flask_jwt_extended import get_jwt_identity, jwt_required


payments = Blueprint("payments", __name__, url_prefix="/api/v1/payments")


@payments.get("/")
@jwt_required()
def get_all():
    #pagination settings 
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    customer_id = get_jwt_identity()

    #Apply fliteres from the Query Params
    amount_gte = request.args.get('amount_gte', 0, type=int)
    amount_lte = request.args.get('amount_lte', 0, type=int)
    invoice_id = request.args.get('invoice', 0, type=int)

    list_payments = []

    #Only apply one filter for query
    if amount_gte > 0:
        payments = Payment.query.filter(Payment.amount >= amount_gte).paginate(page=page, per_page=per_page)
    elif amount_lte > 0:
        payments = Payment.query.filter(Payment.amount <= amount_lte).paginate(page=page, per_page=per_page)
    elif invoice_id > 0:
        payments = Payment.query.filter_by(customer_id=customer_id).paginate(page=page, per_page=per_page)
        for payment in payments.items:
            for invoice in payment.invoices:
                if invoice.id == invoice_id:
                    list_payments.append(
                        {
                            'customer': f"{payment.customer.first_name} {payment.customer.last_name}",
                            'amount': payment.amount,
                            'paid invoices': invoice.id,
                            'created_at': payment.created_at,
                            'updated_at': payment.updated_at,
                        }
                    )

        return jsonify({'payments': list_payments}), HTTP_200_OK

    else:
        payments = Payment.query.filter_by(customer_id=customer_id).paginate(page=page, per_page=per_page)


    for payment in payments.items:
        list_payments.append(
            {
                'customer': f"{payment.customer.first_name} {payment.customer.last_name}",
                'amount': payment.amount,
                'paid invoices': [invoice.id for invoice in payment.invoices],
                'created_at': payment.created_at,
                'updated_at': payment.updated_at,
            }
        )

    #sent meta data to the frontend
    meta = {
        "page": payments.page,
        "pages": payments.pages,
        "total_count": payments.total,
        "has_previous": payments.has_prev,
        "previous": payments.prev_num,
        "has_next": payments.has_next,
        "next": payments.next_num,
    }

    return jsonify({'payments': list_payments, 'meta': meta}), HTTP_200_OK



@payments.post("/")
@jwt_required()
def paid_invoice():

    customer_id = get_jwt_identity()
    amount = request.json.get('amount', 0)
    payment = Payment(customer_id=customer_id, amount=amount)

    invoices_customer = Invoice.query.filter_by(customer_id=customer_id).all()
        

    for invoice in invoices_customer:
        if amount > 0.0 and invoice.remaining_balance > 0.0:
            # fully paid invoice
            if amount >= invoice.remaining_balance:
                invoice.remaining_balance = 0.0
                amount = amount - invoice.remaining_balance
                payment.invoices.append(invoice)

            elif invoice.remaining_balance > 0.0:
                invoice.remaining_balance = invoice.remaining_balance - amount
                amount = 0.0
        elif amount == 0.0:
            break
        elif invoice.remaining_balance == 0.0:
            continue

    db.session.commit()
    

    if payment.amount == 0:
        return jsonify({
            'Message': "Payment applied to one or more invoices.",
        }), HTTP_200_OK
    else:
        return jsonify({
            'Message': "All the invoices was already paid.",
        }), HTTP_200_OK


@payments.get("/<int:id>")
@jwt_required()
def get_payment(id):
    customer_id = get_jwt_identity()
    payment = Payment.query.filter_by(customer_id=customer_id, id=id).first()

    if not payment:
         return jsonify({'message':'payment not found'}),HTTP_404_NOT_FOUND

    return jsonify(
        {
                'customer': f"{payment.customer.first_name} {payment.customer.last_name}",
                'amount': payment.amount,
                'created_at': payment.created_at,
                'updated_at': payment.updated_at,
        }
    ), HTTP_200_OK


@payments.patch('/<int:id>')
@jwt_required()
def edit_payment(id):
    customer_id = get_jwt_identity()
    payment = Payment.query.filter_by(customer_id=customer_id, id=id).first()
    amount = request.get_json().get('amount', 0.0)

    if not payment:
         return jsonify({'message':'payment not found'}),HTTP_404_NOT_FOUND

    payment.amount = amount

    db.session.commit()

    return jsonify(
        {
                'customer': f"{payment.customer.first_name} {payment.customer.last_name}",
                'amount': payment.amount,
                'created_at': payment.created_at,
                'updated_at': payment.updated_at,
        }
    ), HTTP_200_OK


@payments.delete('/<int:id>')
@jwt_required()
def delete_payment(id):
    customer_id = get_jwt_identity()
    payment = Payment.query.filter_by(customer_id=customer_id, id=id).first()
    
    if not payment:
         return jsonify({'message':'payment not found'}),HTTP_404_NOT_FOUND

    db.session.delete(payment)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
