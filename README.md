# Flask-Mercadopago

![PyPI](https://img.shields.io/pypi/v/Flask-Mercadopago)
![PyPI - Downloads](https://img.shields.io/pypi/dm/Flask-Mercadopago)
[![codecov](https://codecov.io/gh/juniors90/Flask-Mercadopago/branch/main/graph/badge.svg?token=ePNLhWhSV7)](https://codecov.io/gh/juniors90/Flask-Mercadopago)
![docstr-cov](https://img.shields.io/endpoint?url=https://api.jsonbin.io/v3/b/62e15eac8ebcdb758843f9af?meta=false)
[![Build status](https://github.com/juniors90/Flask-Mercadopago/actions/workflows/main.yml/badge.svg)](https://github.com/juniors90/Flask-Mercadopago/actions)
[![Documentation Status](https://readthedocs.org/projects/flask-mercadopago/badge/?version=latest)](https://flask-mercadopago.readthedocs.io/en/latest/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/issues)
[![GitHub forks](https://img.shields.io/github/forks/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/network)
[![GitHub stars](https://img.shields.io/github/stars/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/stargazers)
[![GitHub license](https://img.shields.io/github/license/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/juniors90/Flask-Mercadopago?color=green)](https://github.com/juniors90/Flask-Mercadopago/graphs/contributors)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Flask-Mercadopago is a collection of methods for the implementation of Mercado Pago OAuth in Flask.

## Features

- [x] [Authentication generation](https://www.mercadopago.com.ar/developers/en/reference/oauth/_oauth_token/post).
- [x] [Preference generation](https://www.mercadopago.com.ar/developers/en/reference/preferences/_checkout_preferences/post).
- [x] [Checkout Pro integration](https://www.mercadopago.com.ar/developers/en/docs/checkout-pro/landing).


## Requirements

Python 3.8+

## Dependecies for this project.

- [Flask(>=2.0.1)](https://flask.palletsprojects.com/en/2.0.x/) for build the backend.
- [Requests](https://requests.readthedocs.io/en/latest/) for build the backend.
- [mercadopago](https://github.com/mercadopago/sdk-python) for build the backend.

## intallation

You can install via pip:

```cmd
    $> pip install Flask-Mercadopago
```

## Example

Register the extension:

```python
from datetime import datetime
from flask import Flask, jsonify
# To follow the naming rule of Flask extension, although
# this project's name is Flask-Mercadopago, the actual package
# installed is named `flask_mercadopago`.
from flask_mercadopago import Mercadopago

app = Flask(__name__)
app.config["APP_ACCESS_TOKEN"]="APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"
mercadopago = Mercadopago(app)

@app.route("/")
def index():
    card_token_object = {
        "card_number": "4074090000000004",
        "security_code": "123",
        "expiration_year": datetime.now().strftime("%Y"),
        "expiration_month": "12",
        "cardholder": {
            "name": "APRO",
            "identification": {"CPF": "19119119100"},
        },
    }

    card_token_created = mercadopago.card_token().create(card_token_object)

    payment_data = {
        "transaction_amount": 100,
        "token": card_token_created["response"]["id"],
        "description": "Payment description",
        "payment_method_id": 'visa',
        "installments": 1,
        "payer": {
            "email": 'test_user_123456@testuser.com'
        }
    }
    result = mercadopago.payment().create(payment_data)
    payment = result["response"]
    return jsonify(payment) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
```

## Recommended running instructions for dev:

1. Create a virtual environment:

    ```shell script
    $> python3 -m venv venv
    ```

2. Activate the newly created environment:

   On macOS and Linux:
    ```shell script
    $> source venv/bin/activate
    ```
   
   On Windows
   ```
   c:\> .\env\Scripts\activate
   ```

3. Install dependencies:

    ```shell script
    $> (venv) python -m pip install -r requirements/dev.txt
    ```

4. Start the sample app on server locally:

    ```shell script
    $> (venv) python sample_app/app.py
    ```
  
You will get a form like this:

![form rendering](https://raw.githubusercontent.com/juniors90/Flask-Mercadopago/main/docs/source/_static/form.png)

When the validation, the response data will be rendered with proper style:

![validations](https://raw.githubusercontent.com/juniors90/Flask-Mercadopago/main/docs/source/_static/validations.png)
    
## Links

- [Documentation](https://flask-mercadopago.readthedocs.io)
- [Example Application](https://github.com/juniors90/Flask-Mercadopago/tree/main/sample_app)
- [PyPI Releases](https://pypi.org/project/Flask-Mercadopago/)
- [Changelog](https://github.com/juniors90/Flask-Mercadopago/blob/main/CHANGELOG.rst)

## Authors

- Ferreira, Juan David

Please submit bug reports, suggestions for improvements and patches via
the (E-mail: juandavid9a0@gmail.com).

## Contributors

Credits goes to these peoples:

<a href="https://github.com/juniors90/Flask-Mercadopago/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juniors90/Flask-Mercadopago" />
</a>

## Official repository and Issues

- https://github.com/juniors90/Flask-Mercadopago


## License

`Flask-Mercadopago` is free software you can redistribute it and/or modify it
under the terms of the MIT License. For more information, you can see the
[LICENSE](https://github.com/juniors90/Flask-Mercadopago/blob/main/LICENSE) file
for details.
