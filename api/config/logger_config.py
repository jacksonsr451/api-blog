import logging
import os
from logging.config import dictConfig

import colorlog
from pythonjsonlogger import jsonlogger


def configure_logging(is_dev: bool, app_name: str):
    log_level = logging.DEBUG if is_dev else logging.INFO

    log_dir = os.path.join(os.getcwd(), 'logs', app_name)
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f'{app_name}.log')
    json_log_file = os.path.join(log_dir, f'{app_name}_structured.log')

    colored_formatter = colorlog.ColoredFormatter(
        f'%(log_color)s%(asctime)s%(reset)s - {app_name} - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'green',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    json_formatter = jsonlogger.JsonFormatter(
        f'%(asctime)s {app_name} %(levelname)s %(message)s',
        rename_fields={
            'asctime': 'timestamp',
            'levelname': 'level',
            'message': 'msg',
        },
    )

    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': f'%(asctime)s - {app_name} - %(levelname)s - %(message)s'
                },
                'colored': {
                    '()': colorlog.ColoredFormatter,
                    'format': f'%(log_color)s%(asctime)s%(reset)s - {app_name} - %(log_color)s%(levelname)s%(reset)s - %(message)s',
                    'log_colors': {
                        'DEBUG': 'green',
                        'INFO': 'cyan',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    },
                },
                'json': {
                    '()': jsonlogger.JsonFormatter,
                    'format': f'%(asctime)s {app_name} %(levelname)s %(msg)s %(pathname)s %(lineno)d',
                },
            },
            'handlers': {
                'console': {
                    'level': log_level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'colored',
                },
                'file': {
                    'level': log_level,
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': log_file,
                    'when': 'midnight',
                    'backupCount': 7,
                    'formatter': 'default',
                },
                'json_file': {
                    'level': log_level,
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': json_log_file,
                    'when': 'midnight',
                    'backupCount': 7,
                    'formatter': 'json',
                },
            },
            'loggers': {
                'api_gateway': {
                    'level': log_level,
                    'handlers': ['console', 'file', 'json_file'],
                    'propagate': False,
                },
                'uvicorn': {
                    'level': logging.INFO,
                    'handlers': ['console'],
                    'propagate': False,
                },
                'uvicorn.error': {
                    'level': logging.INFO,
                    'handlers': ['console'],
                    'propagate': False,
                },
                'uvicorn.access': {
                    'level': logging.INFO,
                    'handlers': ['console'],
                    'propagate': False,
                },
            },
        }
    )

    logger = logging.getLogger('api_gateway')
    logger.info('Logging configured successfully')

    return logger