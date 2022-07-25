Flask-Mercadopago
=================

.. only:: html

    .. image:: https://img.shields.io/github/issues/juniors90/Flask-Mercadopago
        :alt: GitHub issues
        :target: https://github.com/juniors90/Flask-Mercadopago/issues
    
    .. image:: https://img.shields.io/github/forks/juniors90/Flask-Mercadopago
        :alt: GitHub forks
        :target: https://github.com/juniors90/Flask-Mercadopago/network
    
    .. image:: https://img.shields.io/github/stars/juniors90/Flask-Mercadopago
        :alt: GitHub stars
        :target: https://github.com/juniors90/Flask-Mercadopago/stargazers
    
    .. image:: https://img.shields.io/github/license/juniors90/Flask-Mercadopago
        :alt: GitHub license
        :target: https://github.com/juniors90/Flask-Mercadopago/blob/main/LICENSE
    
    .. image:: https://img.shields.io/github/contributors/juniors90/Flask-Mercadopago?color=green
        :alt: GitHub contributors
        :target: https://github.com/juniors90/Flask-Mercadopago/graphs/contributors
    
    .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :alt: Code style
        :target: https://github.com/psf/black

Features
--------

- A features.


Requirements
~~~~~~~~~~~~~

- Python 3.8+

Dependecies for this project.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Flask(>=2.0.1) <https://flask.palletsprojects.com/en/2.0.x/>`_ for build the backend.
- `Requests(>=2.28.1) <https://requests.readthedocs.io/en/latest/>`_ for build the backend.

Intallation
~~~~~~~~~~~

You can install via pip:

.. code-block::

    $> pip install Flask-Mercadopago


Example
~~~~~~~

Register the extension:

.. code-block:: python

    from flask import Flask
    # To follow the naming rule of Flask extension, although
    # this project's name is Flask-Mercadopago, the actual package
    # installed is named `flask_mercadopago`.
    from flask_mercadopago import Mercadopago
    app = Flask(__name__)
    mercadopago = Mercadopago(app)


Now with the `render_ui_form` macro:

.. code-block:: html

     <html>
     <head>
          <!-- Mercado Pago SDK JS -->
          {{ merccadopago.load_js() }}
      </head>
      <body>
          <h2>Login</h2>
      </body>
      </html>

Read the `Basic Usage <https://flask-mercadopago.readthedocs.io/en/latest/notes/basic.html>`_ 
docs for more details.

Links
~~~~~

- `Documentation <https://flask-mercadopago.readthedocs.io>`_
- `Example Application <https://github.com/juniors90/Flask-Mercadopago/tree/main/sample_app>`_
- `PyPI Releases <https://pypi.org/project/Flask-Mercadopago/>`_
- `Changelog <https://github.com/juniors90/Flask-Mercadopago/blob/main/CHANGELOG.rst>`_


Authors
~~~~~~~

- Ferreira, Juan David

Please submit bug reports, suggestions for improvements and patches via
the (E-mail: juandavid9a0@gmail.com).

Contributors
~~~~~~~~~~~~

Credits goes to these peoples:

.. raw:: html

    <a href="https://github.com/juniors90/Flask-Mercadopago/graphs/contributors">
        <img src="https://contrib.rocks/image?repo=juniors90/Flask-Mercadopago" />
    </a>

Official repository and Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- https://github.com/juniors90/Flask-Mercadopago


License
~~~~~~~

`Flask-Mercadopago` is free software you can redistribute it and/or modify it
under the terms of the MIT License. For more information, you can see the
`LICENSE <https://github.com/juniors90/Flask-Mercadopago/blob/main/LICENSE>`_ file
for details.