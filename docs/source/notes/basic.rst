Basic Usage
===========

Installation
------------

Create a project folder and a :file:`venv` folder within:

.. tabs::

   .. group-tab:: macOS/Linux

      .. code-block:: text

         $ mkdir myproject
         $ cd myproject
         $ python3 -m venv venv

   .. group-tab:: Windows

      .. code-block:: text

         > mkdir myproject
         > cd myproject
         > py -3 -m venv venv


Activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

Before you work on your project, activate the corresponding environment:

.. tabs::

   .. group-tab:: macOS/Linux

      .. code-block:: text

         $ source venv/bin/activate

   .. group-tab:: Windows

      .. code-block:: text

         > .\venv\Scripts\activate

Your shell prompt will change to show the name of the activated
environment.


Install Flask-Mercadopago
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ pip install Flask-Mercadopago


Initialization
--------------

.. code-block:: python

    from flask import Flask
    from flask_mercadopago import Mercadopago

    app = Flask(__name__)

    mercadopago = Mercadopago(app)

