# Flask-Mercadopago

[![codecov](https://codecov.io/gh/juniors90/Flask-Mercadopago/branch/main/graph/badge.svg?token=ePNLhWhSV7)](https://codecov.io/gh/juniors90/Flask-Mercadopago)
![docstr-cov](https://img.shields.io/endpoint?url=https://jsonbin.io/juniors90/Flask-Mercadopago/badges/docstr-cov)
[![Build status](https://github.com/juniors90/Flask-Mercadopago/actions/workflows/main.yml/badge.svg)](https://github.com/juniors90/Flask-Mercadopago/actions)
[![GitHub issues](https://img.shields.io/github/issues/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/issues)
[![GitHub forks](https://img.shields.io/github/forks/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/network)
[![GitHub stars](https://img.shields.io/github/stars/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/stargazers)
[![GitHub license](https://img.shields.io/github/license/juniors90/Flask-Mercadopago)](https://github.com/juniors90/Flask-Mercadopago/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/juniors90/Flask-Mercadopago?color=green)](https://github.com/juniors90/Flask-Mercadopago/graphs/contributors)

Flask-Mercadopago is a collection of functions. 

## Features

- [x] Authentication generation.
- [x] Preference generation.


## Requirements

Python 3.8+

## Dependecies for this project.

- [Flask(>=2.0.1)](https://flask.palletsprojects.com/en/2.0.x/) for build the backend.
- [Requests](https://requests.readthedocs.io/en/latest/) for build the backend.

## intallation

You can install via pip:

```cmd
    $> pip install Flask-Mercadopago
```

## Example

Register the extension:

```python
from flask import Flask
# To follow the naming rule of Flask extension, although
# this project's name is Flask-Mercadopago, the actual package
# installed is named `flask_mercadopago`.
from flask_mercadopago import Mercadopago

app = Flask(__name__)
mercadopago = Mercadopago(app)
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

![form rendering](https://github.com/juniors90/Flask-Mercadopago/blob/main/docs/source/notes/res/Captura%20de%20pantalla%202022-07-24%20222359.png)

When the validation, the response data will be rendered with proper style:

![error form rendering](https://github.com/juniors90/Flask-Mercadopago/blob/main/docs/source/notes/res/Captura%20de%20pantalla%202022-07-24%20222732.png)
    
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
