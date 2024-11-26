import subprocess

from api.config.settings import settings


def run():
    command = f'uvicorn api.main:app --host 0.0.0.0 --port {settings.SERVER_PORT} --reload'

    try:
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            exit(result.returncode)
    except KeyboardInterrupt:
        print('\nServer interrupted by user. Shutting down gracefully.')
        exit(0)
