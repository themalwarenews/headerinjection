import sys
import subprocess
from pyfiglet import Figlet

def print_colored_message(color_code, message):
    colors = {
        'red': '\033[31m',
        'green': '\033[32m'
    }
    color = colors.get(color_code, '\033[0m')
    print(color + message + '\033[0m')

def is_command_installed(command):
    result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def verify_dependencies():
    dependencies = ['curl']
    for dependency in dependencies:
        if not is_command_installed(dependency):
            print(f"The dependency {dependency} is not installed.")
            return False
    return True

def execute_subprocess(command):
    try:
        return subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"An error occurred while executing {command}: {e}")
        return None

def is_url_vulnerable_to_injection(url, headers):
    for header in headers:
        cmd = ['curl', '--head', '--max-time', '10', '-s', '-H', f'{header}: iamsharan.com', url]
        response = execute_subprocess(cmd)
        if response and "iamsharan.com" in response.stdout:
            return True, header
    return False, None

def create_ascii_banner(text):
    f = Figlet(font='slant')
    ascii_art = f.renderText(text)
    print(ascii_art)

def main():
    create_ascii_banner('Header Injection')

    if not verify_dependencies():
        print("Please make sure the following dependencies are installed: curl.")
        sys.exit(1)

    headers = [
        "Host",
        "X-Forwarded-Host",
        "X-Client-IP",
        "X-Remote-IP",
        "X-Remote-Addr",
        "X-Host",
        "X-Originating-IP",
        "X-Forwarded-For",
        "X-Real-IP"
    ]

    if len(sys.argv) < 3:
        print("Invalid command. Usage: script.py -f file.txt OR script.py -d domain.com")
        sys.exit(1)

    urls = None
    if sys.argv[1] == "-f":
        with open(sys.argv[2], 'r') as f:
            urls = [line.strip() for line in f]
    elif sys.argv[1] == "-d":
        urls = [sys.argv[2]]
    else:
        print("Invalid command. Usage: script.py -f file.txt OR script.py -d domain.com")
        sys.exit(1)

    for url in urls:
        is_vulnerable, payload = is_url_vulnerable_to_injection(url, headers)
        if is_vulnerable:
            print_colored_message("red", f"{url} is vulnerable to Host Header Injection with the header: {payload}")
        else:
            print_colored_message("green", f"{url} is not vulnerable to Host Header Injection")

if __name__ == "__main__":
    main()
