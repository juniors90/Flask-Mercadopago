Configurations
==============

.. ifconfig:: show_github_hote
    
    A list of configuration keys for this extension:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

+--------------------------------+-----------------------------------------------------------------------------+
| Configuration Variable         | Description                                                                 |
+================================+=============================================================================+
| APP_ACCESS_TOKEN               | The production credentials for your ACCESS TOKEN application \              |
|                                | given by `Mercadopago`_. Default: ``None``.                                 |
+--------------------------------+-----------------------------------------------------------------------------+
| AUTHORIZATION_ENDPOINT         | The authorization endpoint resources URL.\                                  |
|                                | Default: ``"https://auth.mercadopago.com.ar/authorization"``.               |
+--------------------------------+-----------------------------------------------------------------------------+
| BASE_URL                       | Base url for To make requests.\                                             |
|                                | Default: ``"https://api.mercadopago.com/v1"``.                              |
+--------------------------------+-----------------------------------------------------------------------------+
| CALLBACK_URL                   | The URI(s) user are redirected to after authentication/authorization.\      |
|                                | Default: ``None``.                                                          |
+--------------------------------+-----------------------------------------------------------------------------+
| CLIENT_ID                      | The values for your ClientID application given by Mercadopago_ application. |
|                                | Default: ``None``.                                                          |
+--------------------------------+-----------------------------------------------------------------------------+
| CLIENT_SECRET                  | The value for your Client SECRET application given by `Mercadopago`_.       |
|                                | Default: ``None``.                                                          |
+--------------------------------+-----------------------------------------------------------------------------+
| ORG_CONNECTION_COMPLETED_URL   | General link to your home page. Default: ``None``.                          |
+--------------------------------+-----------------------------------------------------------------------------+
| RESPONSE_TYPE                  | The response type. Default: ``"code"``.                                     |
+--------------------------------+-----------------------------------------------------------------------------+
| STATE                          | An UUID strin for each equest an authorization code. Default: ``None``.     |
+--------------------------------+-----------------------------------------------------------------------------+
| TOKEN_ENDPOINT                 | The authorization endpoint resources URL.\                                  |
|                                | Default: ``"https://api.mercadopago.com/oauth/token"``.                     |
+--------------------------------+-----------------------------------------------------------------------------+

.. _Mercadopago: https://www.mercadopago.com.ar/developers/en
