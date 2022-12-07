from src.constants.http_status_codes import *
from flask import Blueprint, request, jsonify
from src.database import Invoice
from flask_jwt_extended import get_jwt_identity, jwt_required


invoices = Blueprint("invoices", __name__, url_prefix="/api/v1/invoices")


@invoices.get("/")
@jwt_required()
def get_all_invoices():
    #pagination settings 
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)


    customer_id = get_jwt_identity()
    invoices = Invoice.query.filter_by(customer_id=customer_id).paginate(page=page, per_page=per_page)

    list_invoices = []

    for invoice in invoices.items:
        list_invoices.append(
            {
                'customer': f"{invoice.customer.first_name} {invoice.customer.last_name}",
                'amount': invoice.amount,
                'remaining_balance': invoice.remaining_balance,
                'created_at': invoice.created_at,
                'updated_at': invoice.updated_at,
            }
        )

    #sent meta data to the frontend
    meta = {
        "page": invoices.page,
        "pages": invoices.pages,
        "total_count": invoices.total,
        "has_previous": invoices.has_prev,
        "previous": invoices.prev_num,
        "has_next": invoices.has_next,
        "next": invoices.next_num,
    }

    return jsonify({'invoices': list_invoices, 'meta': meta}), HTTP_200_OK



@invoices.get("/<int:id>")
@jwt_required()
def get_invoice(id):
    customer_id = get_jwt_identity()
    invoice = Invoice.query.filter_by(customer_id=customer_id, id=id).first()

    if not invoice:
         return jsonify({'message':'Invoice not found'}),HTTP_404_NOT_FOUND

    return jsonify(
        {
                'customer': f"{invoice.customer.first_name} {invoice.customer.last_name}",
                'amount': invoice.amount,
                'remaining_balance': invoice.remaining_balance,
                'created_at': invoice.created_at,
                'updated_at': invoice.updated_at,
        }
    ), HTTP_200_OK
