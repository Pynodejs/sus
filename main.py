import os
import requests
import random
import threading
import json
from zoneinfo import ZoneInfo
from colorama import Fore
from datetime import datetime

def center(var: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class Console:
    def ui(self):
        os.system(f'cls && title [DNG] Discord Nitro Generator' if os.name == "nt" else "clear")
        print(center(f"""
██████╗ ███╗   ██╗ ██████╗ 
██╔══██╗████╗  ██║██╔════╝            ~ Discord Nitro Generator ~
██║  ██║██╔██╗ ██║██║  ███╗     
██║  ██║██║╚██╗██║██║   ██║     github.com/kanekiWeb ~ skulldev.ga
██████╔╝██║ ╚████║╚██████╔╝ 
╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ \n\n
              """).replace('█', Fore.CYAN + "█" + Fore.RESET).replace('~', Fore.CYAN + "~" + Fore.RESET).replace('-', Fore.CYAN + "-" + Fore.RESET))
    
    def printer(self, color, status, code):
        with threading.Lock():
            print(f"[ {datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%H:%M:%S')} {color} {status} {Fore.RESET}] {color}> {Fore.RESET}discord.gift/{code}")
    
    def proxies_count(self):
        with open('config/proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file]
        return len(proxies)

class Worker:
    def random_proxy(self):
        with open('config/proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f]
        return random.choice(proxies)

    def config(self, key, subkey=None):
        with open('config/config.json', 'r') as conf:
            data = json.load(conf)
        return data[key] if subkey is None else data[key].get(subkey, "")
    
    def run(self):
        self.code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
        try:
            req = requests.get(
                f'https://discord.com/api/v10/entitlements/gift-codes/{self.code}?with_application=false&with_subscription_plan=true',
                proxies={
                    'http': self.config("proxies") + '://' + self.random_proxy(),
                    'https': self.config("proxies") + '://' + self.random_proxy()
                },
                timeout=5
            )
            
            if req.status_code == 200:
                Console().printer(Fore.LIGHTGREEN_EX, "Valid", self.code)
                with open('results/hit.txt', 'a+') as f:
                    f.write(self.code + "\n")
                try:
                    requests.post(
                        self.config("valid", "url"),
                        json={
                            "content": f"||@here|| **__New Valid Nitro !!__**\n\nhttps://discord.gift/{self.code}",
                            "username": self.config("valid", "username"),
                            "avatar_url": self.config("valid", "avatar")
                        }
                    )
                except:
                    pass
            elif req.status_code == 404:
                Console().printer(Fore.LIGHTRED_EX, "Invalid", self.code)
                try:
                    requests.post(
                        self.config("unchecked", "url"),
                        json={
                            "content": f"**__New Unchecked Nitro !!__**\n\nhttps://discord.gift/{self.code}",
                            "username": self.config("unchecked", "username"),
                            "avatar_url": self.config("unchecked", "avatar")
                        }
                    )
                except:
                    pass
            elif req.status_code == 429:
                Console().printer(Fore.LIGHTBLUE_EX, "Rate Limited", self.code)
                try:
                    requests.post(
                        self.config("unchecked", "url"),
                        json={
                            "content": f"**__New Unchecked Nitro !!__**\n\nhttps://discord.gift/{self.code}",
                            "username": self.config("unchecked", "username"),
                            "avatar_url": self.config("unchecked", "avatar")
                        }
                    )
                except:
                    pass
            else:
                Console().printer(Fore.LIGHTYELLOW_EX, "Retry", self.code)
        
        except KeyboardInterrupt:
            Console().ui()
            with threading.Lock():
                print(f"{Fore.LIGHTRED_EX} Stopped > {Fore.RESET}Nitro Gen Stopped by Keyboard Interrupt.")
            os.system('pause >nul')
            exit()
        except Exception as e:
            return

if __name__ == "__main__":
    console = Console()
    console.ui()
    print(" " + Fore.CYAN + str(console.proxies_count()) + Fore.RESET + " Total proxies loaded...\n\n")
    worker = Worker()
    
    while True:
        if threading.active_count() <= int(worker.config("thread")):
            threading.Thread(target=worker.run).start()
