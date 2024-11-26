import subprocess


def run():
    commands = [
        'isort .',
        'blue .',
    ]
    for command in commands:
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            exit(result.returncode)
