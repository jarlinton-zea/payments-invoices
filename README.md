# Invoice Payments


# Built with

  - Python 3.7
  - Flask
  - SQLALCHEMY


#  Features!

  - Customers can create an account and log in.
  - A customers base invoices (100 invoices) will create at the registration state.
  - Customers can applied a full or partially payment to **one or more** Invoices.

  


## Installation

Install `pipenv` enviroment manager.

```
brew install pipenv
```
 Navigate to the application directory:

```
git clone https://github.com/jarlinton-zea/payments-invoices.git
cd payments-invoices
git checkout main
```

Then Activate the venv using:
```
mkdir .venv
pipenv shell
```

Install the application package dependencies with:

```
pipenv install -r requirements.txt
```

Run the application with:

```
flask run
```


#### URL endpoints

| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
|   `api/v1/auth/register` | `POST` |  Creates a new Customer, and add 100 invoices for that Customer |
|   `api/v1/auth/login` | `POST` |  Log in a Customer |
| `api/v1/invoices` | `GET` | Retrieve all the invoices for a specific customer |
| `api/v1/invoices/<int:id>` | `GET` | Retrieves a specific invoice
|  `api/v1/payments/`          | `POST` | Creates a new payment for a logged customer
| `api/v1/payments/<int:id>/` | `GET` | Gets a specific payment
|  `api/v1/payments/<int:id>/` | `GET` | Gets all the associate payments to a customer
|  `api/v1/payments/<int:id>/` | `DELETE` | Deletes a specific payment
|  `api/v1/payments/<int:id>/` | `PATCH` | Updates a specific payment
  

#### Example New Customer body
```
{
    "first_name": "Jazlin",
    "last_name": "Moreno",
    "email": "jazlin.moreno@outlook.com",
    "password": "$$MariaLeticia13$$"
}
```

#### Example to log with a registered customer
```
{
   "email": "jazlin.moreno@outlook.com",
    "password": "$$MariaLeticia13$$"
}
```

#### Example Create/Update Payment Body
```
{
    "amount": 49800
}
```


Note >>> Import post collection from: ``` postman/Payments_againt_Invoices.postman_collection.json```


License
---
MIT
## Author
[Jarlinton Moreno](https://github.com/jarlinton-zea)