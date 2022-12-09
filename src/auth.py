import validators
from src.constants.http_status_codes import *
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import Customer, db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from src.utils import dump_data
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
@swag_from("./docs/auth/register.yaml")
def register():
    first_name = request.json.get("first_name", "")
    last_name = request.json.get("last_name", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    if len(password) < 6:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(first_name) < 3 and len(last_name) < 3:
        return jsonify({"error": "Username is too short"}), HTTP_400_BAD_REQUEST

    if any(char.isdigit() for char in first_name) or " " in first_name:
        return (
            jsonify(
                {"error": "First name couldn't have digits inside it, or have spaces."}
            ),
            HTTP_400_BAD_REQUEST,
        )

    if any(char.isdigit() for char in last_name):
        return (
            jsonify(
                {"error": "Last name couldn't have digits inside it, or have spaces."}
            ),
            HTTP_400_BAD_REQUEST,
        )

    if not validators.email(email):
        return jsonify({"error": "Email is not valid."}), HTTP_400_BAD_REQUEST

    user_email = Customer.query.filter_by(email=email).first()

    if user_email is not None:
        return (
            jsonify({"error": "Email already be assigned to another user."}),
            HTTP_409_CONFLICT,
        )

    # Generate user's credentials after validations.
    pwd_hash = generate_password_hash(password)

    # save new user on the database.
    customer = Customer(
        first_name=first_name, last_name=last_name, password=pwd_hash, email=email
    )
    db.session.add(customer)
    db.session.commit()

    # Generate dump data for customer after registration on the database...
    db.session.add_all(dump_data(customer_id=customer.id))
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Customer created",
                "user": {"name": f"{first_name} {last_name}", "email": email},
            }
        ),
        HTTP_201_CREATED,
    )


@auth.post("/login")
@swag_from("./docs/auth/login.yaml")
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    customer = Customer.query.filter_by(email=email).first()

    if customer:
        is_pass_correct = check_password_hash(customer.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=customer.id)
            access = create_access_token(identity=customer.id)

            return (
                jsonify(
                    {
                        "refresh": refresh,
                        "access": access,
                        "user": f"{customer.first_name} {customer.last_name}",
                        "email": customer.email,
                    }
                ),
                HTTP_200_OK,
            )
    return jsonify({"error": "Wrong credentials"}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    customer_id = get_jwt_identity()
    customer = Customer.query.filter_by(id=customer_id).first()

    return (
        jsonify(
            {
                "user": f"{customer.first_name} {customer.last_name}",
                "email": customer.email,
            }
        ),
        HTTP_202_ACCEPTED,
    )


@auth.get("/token/refresh")
@jwt_required()
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access token": access}), HTTP_200_OK
