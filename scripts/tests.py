import subprocess
from colorama import init, Fore

init(autoreset=True)

def run_tests():
    result = subprocess.run(
        ['poetry', 'run', 'pytest', '-vvv'],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    
    if result.stderr:
        print(Fore.RED + result.stderr)

    if result.returncode == 0:
        print(Fore.GREEN + "All tests passed successfully!")
    else:
        print(Fore.RED + "Some tests failed.")
