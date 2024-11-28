import importlib
import logging
import os
import sys
from os.path import abspath, dirname

from decouple import config as env_config
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context
from api.config.settings import settings

sys.path.append(dirname(dirname(abspath(__file__))))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('alembic')
logger.setLevel(logging.DEBUG)

config = context.config
config.set_main_option('sqlalchemy.url', settings.POSTGRES_URL)

models_directory = 'infrastructure/models'

for filename in os.listdir(models_directory):
    if filename.endswith('_model.py'):
        module_name = filename[:-3]
        try:
            app_module = importlib.import_module(
                f'infrastructure.models.{module_name}'
            )
            logger.info(f'Models loaded from {module_name}')
        except ModuleNotFoundError:
            logger.warning(f'Could not load models from {module_name}')

target_metadata = SQLModel.metadata


def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    logger.debug(f'Using URL: {url}')
    context.configure(url=url, target_metadata=target_metadata)
    with context.begin_transaction():
        logger.info('Starting offline migration...')
        context.run_migrations()
        logger.info('Offline migration completed.')


def run_migrations_online():
    logger.info('Running migrations online...')
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        logger.debug('Database connection established.')
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            logger.info('Starting database migration transaction...')
            context.run_migrations()
            logger.info('Database migration transaction completed.')


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
