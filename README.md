# Vendor Management System

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/srishtigupta91/vendor_management.git
$ cd vendor_management
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3.12 env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd vendor_management
```

## Create a Database

## Migration Commands
In order to insert any data in database, you need to create a database 
and migrate the database with the following commands.

```
(env)$ python manage.py makemigrations vendor orders performance
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/auth/users/create/`.

In order to test the authentication flows, fill in the account details in
`vendor_management/auth/views.py` to create your credentials.

## Authentication

First you need to authenticate the users and add the authenicate token to
consume other apis.

Headers: `{Authorization: Token generated_token_id}`

To generate the token you need to call the below api:

Login API: `http://127.0.0.1:8000/auth/api-token-auth/`

Payload: `{"username": "admin", "password": "admin@123"}`

Example:
 While calling this api you will get the response in this format.

`{
    "token": "8166695b7318f72c0e50f85f8f62d3d2c8c4a0ae"
}`


## Walkthrough

## Vendor Profile Creation
 
Now you can create the vendors profile by navigating the following url:
`http://127.0.0.1:8000/api/vendors/`

Headers: `{
    "Authorization": "Token 8166695b7318f72c0e50f85f8f62d3d2c8c4a0ae"
}`

Payload Passed to generate the Vendor Profile:

`{
    "vendor_code": "1001",
    "vendor_name": "Prestiage",
    "contact_number": "9827676761",
    "address": "Kalyan Shil Road, Dombivli East"
}`

Method: GET, POST

Response:
`[
    {
        "id": 1,
        "vendor_code": "1001",
        "vendor_name": "Prestiage",
        "contact_number": "9827676761",
        "address": "Kalyan Shil Road, Dombivli East",
        "on_time_delivery_rate": 1.0,
        "quality_rating_avg": 3.5,
        "average_response_time": 20.0,
        "fulfillment_rate": 3.0
    }
]`

### Purchase Order Creation

#### Items Creation API

For Generating the purchase order of the specific vendor you would require some items
summary. Using the below api you can create multiple items.
`http://127.0.0.1:8000/api/purchase_orders/items`

Headers: `{
    "Authorization": "Token 8166695b7318f72c0e50f85f8f62d3d2c8c4a0ae"
}`

Methods: GET, POST, PATCH, DELETE

Payload passed to generate the Items:
`{
    "serial_no": "1",
    "item_name": "Prestige Electric Kettle",
    "item_description": "1.2 Lts Prestige Electric Kettle",
    "size": "1.2 ltr  (19 cm * 18.5 cm * 21 cm)",
    "price": 654.0
}`

Response Received:

`[
    {
        "id": 1,
        "serial_no": "1",
        "item_name": "Prestige Electric Kettle",
        "item_description": "1.2 Lts Prestige Electric Kettle",
        "size": "1.2 ltr  (19 cm * 18.5 cm * 21 cm)",
        "price": 654.0
    }
]`
#### Purchase Order Creation API

After Creating Vendor Profile and list of Items for generating orders. 
You need to generate the orders by navigating the following url:
`http://127.0.0.1:8000/api/purchase_orders/`

Headers: `{
    "Authorization": "Token 8166695b7318f72c0e50f85f8f62d3d2c8c4a0ae"
}`

Payload Passed to generate the Purchase Orders:

`{
    "po_number": "2",
    "order_date": "2023-12-05T08:30:23.357595Z",
    "delivery_date": "2023-12-05T13:59:00Z",
    "quantity": 21,
    "status": 1,
    "issue_date": "2023-12-05T08:30:23.357739Z",
    "vendor": 1,
    "items": 1
}`

Method: GET, POST

Response:
`[
    {
        "id": 1,
        "po_number": "2",
        "order_date": "2023-12-05T08:30:23.357595Z",
        "delivery_date": "2023-12-05T13:59:00Z",
        "quantity": 21,
        "status": 1,
        "issue_date": "2023-12-05T08:30:23.357739Z",
        "vendor": 1,
        "items": 1
    }
]`


### Acknowledgement Of the Issued Orders:

Once the order is placed, we should get the acknowledgement from the vendor
to received to orders. The following api is used to update the acknowledgement date
of the issued order.

`http://127.0.0.1:8000/api/purchase_orders/acknowledgement/`

Headers: `{
    "Authorization": "Token 8166695b7318f72c0e50f85f8f62d3d2c8c4a0ae"
}`

Payload Passed to generate the Purchase Orders:

`{
    "po_number": "722",
    "acknowledgment_date": "2023-09-12T09:00:00Z"
}`

Method: GET, POST

Response:
`{
    "po_number": "722",
    "acknowledgment_date": "2023-09-12T09:00:00Z"
}`

### Update the Purchase order status

Update the status of the purchase order by using the following api:
`http://127.0.0.1:8000/api/purchase_orders/<po_number>`

Headers: `{
    "Authorization": "Token 8166695b7318f72c0e50f85f8f62d3d2c8c4a0ae"
}`

Payload Passed to generate the Purchase Orders:

`{
    "po_number": "2",
    "status": 1
}`

Method: GET, POST

Response:
`{
    "po_number": "121",
    "status": 1,
    "vendor": {
        "name": "R for Rabbit",
        "vendor_code": "1002",
        "on_time_delivery_rate": 0.0
    }
}`


## Tests

You will find all test cases under the tests folder. We have used the pytest for
testing this application.

These are the following commands to run the unittests:

To run all test cases:

```sh
(env)$ pytest -s
```

To run a single Test case, you need to pass the file name to run the test case :
eg:
```sh
(env)$ pytest -k "test_create_vendors"
```
