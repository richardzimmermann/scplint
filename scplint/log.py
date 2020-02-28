'''
Default logging setup and configuration for modules. Setup is for example:

.. highlight:: py
.. code-block:: py

    logger = log.init_logging('INFO')

-------
'''

import json
import logging.config
import time
from datetime import datetime
from decimal import Decimal
from logging import getLogger


class CustomEncoder(json.JSONEncoder):
    ''' Enable json.dumps to use decimals and datetime '''
    def default(self, o):  # pylint: disable=E0202
        ''' Converts given datatypes into dynamodb compatible datatypes '''
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%dT%H:%M:%S")
        if isinstance(o, Decimal):
            return float(o)
        return super(CustomEncoder, self).default(o)


def init_logging(log_level: str = 'DEBUG',
                 formatter: str = 'json') -> getLogger:
    ''' Returns a pre-configured logger for console output and optional log
    file output.

    Args:
        log_level (str): the target debuging level for logs
        formatter (str): the target format for the logs. pre-defined formats
            are `json`, `console` and `file`

    Returns:
        logger (object): the logger object

    Examples:

    log format `json`:

    .. highlight:: json
    .. code-block:: json

        {
            "msg": "import logging",
            "level": "INFO",
            "file": "log.py",
            "line": 47,
            "module": "log",
            "func": "init_logging"
        }

    Log format `console` (without leading time stamp):

    .. highlight:: bash
    .. code-block:: bash

        INFO     47  log.init_logging: import logging


    Log format `file`:

    .. highlight:: bash
    .. code-block:: bash

        2018-12-06 11:29:31,935Z INFO     47  log.init_logging: import logging

    Log level can be configured with numbers (``10``, ``20``, ``30``, ``40``)
    or with level names (``DEBUG``, ``INFO``, ``WARN``, ``ERROR``).
    '''

    logconfig = {
        'version': 1,
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': formatter
            }
        },
        'formatters': {
            'json': {
                'format': ('{"msg":"%(message)s","level":"%(levelname)s",'
                           '"file":"%(filename)s","line":%(lineno)d,'
                           '"module":"%(module)s","func":"%(funcName)s"}')
            },
            'console': {
                'format': ('%(levelname)-8s %(lineno)-3d'
                           ' %(module)s.%(funcName)s: %(message)s')
            },
            'file': {
                'format': ('%(asctime)s.%(msecs)03dZ'
                           ' %(levelname)-8s %(lineno)-3d'
                           ' %(module)s.%(funcName)s: %(message)s'),
                'datefmt': '%Y-%m-%dT%H:%M:%S'
            }
        },
        'root': {
            'handlers': ['stdout'],
            'level': log_level
        }
    }

    logging.Formatter.converter = time.gmtime
    logging.config.dictConfig(logconfig)
    logger = getLogger(__name__)

    logger.debug('configure logging with loglevel=%s', log_level)
    return logger


def return_http_response(statuscode: str, statusmessage: [str, dict]) -> dict:
    ''' returns the http status for result handling

    Args:
        statuscode (str): the status code for your operation
        statusmessage (str/dict): information about your operation as simple
            string or dictionary. if you hand over a dictionary, we recommend
            to add the key 'message' with a single line status messsage.

    Returns:
        response (dict):
        a dictionary with header, statuscode and result information

    Example Return:

    .. highlight:: json
    .. code-block:: json

        {
            "statusCode": "200",
            "body": "{\\"message\\": \\"route 53 resolver rules are as...\\"}",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    '''

    if isinstance(statusmessage, dict):
        message = statusmessage
    else:
        message = {'message': str(statusmessage)}

    response = {
        'statusCode': statuscode,
        'body': json.dumps(message, cls=CustomEncoder),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    return response
