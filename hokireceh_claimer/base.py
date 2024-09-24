import os
import sys
from colorama import init, Fore, Style
import json
from datetime import datetime
import requests
from requests.auth import HTTPProxyAuth

init(autoreset=True)

class Base:
    def __init__(self):
        self.red = Fore.LIGHTRED_EX
        self.yellow = Fore.LIGHTYELLOW_EX
        self.green = Fore.LIGHTGREEN_EX
        self.black = Fore.LIGHTBLACK_EX
        self.blue = Fore.LIGHTBLUE_EX
        self.white = Fore.LIGHTWHITE_EX
        self.reset = Style.RESET_ALL

    def file_path(self, file_name: str):
        caller_dir = os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename))
        return os.path.join(caller_dir, file_name)

    def create_line(self, length=50):
        return "-" * length

    def create_banner(self, game_name: str):
        banner = f"""{Fore.GREEN}
╭╮╭┳┳╮╱╱╱╱╭━╮╱╱╱╱╱╱╱╱╭╮
┃╰╯┃╭╯╭━━╮┃╋┣┳┳━┳┳━┳━┫╰╮
┃╭╮┃╰╮╰━━╯┃╭┫╭┫╋┣┫┻┫━┫╭┫
╰╯╰┻┻╯╱╱╱╱╰╯╰╯╰┳╯┣━┻━┻━╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━╯                                
    Auto Claim for {game_name} - Mini Apps
    Author  : Team Gabut
    Github  : https://github.com/hokireceh
    Telegram: https://t.me/garapanairdrop_indonesia
        {Style.RESET_ALL}"""
        return banner

    def get_config(self, config_file: str, config_name: str):
        try:
            with open(config_file, "r") as file:
                config = json.load(file)
                return config.get(config_name, "false").lower() == "true"
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.log(f"{self.red}Error reading config file: {self.white}{e}")
            return False

    def clear_terminal(self):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{self.black}[{now}]{self.reset} {msg}{self.reset}")

    def format_proxy(self, proxy_info):
        return {"http": f"{proxy_info}", "https": f"{proxy_info}"}

    def check_ip(self, proxy_info):
        url = "https://api.ipify.org?format=json"
        proxies = self.format_proxy(proxy_info=proxy_info)

        if "@" in proxy_info:
            proxy_credentials = proxy_info.split("@")[0]
            proxy_user, proxy_pass = proxy_credentials.split(":")[1:3]
            auth = HTTPProxyAuth(proxy_user, proxy_pass)
        else:
            auth = None

        try:
            response = requests.get(url=url, proxies=proxies, auth=auth)
            response.raise_for_status()
            actual_ip = response.json().get("ip")
            self.log(f"{self.green}Actual IP Address: {self.white}{actual_ip}")
            return actual_ip
        except requests.exceptions.RequestException as e:
            self.log(f"{self.red}IP check failed: {self.white}{e}")
            return None

    def parse_proxy_info(self, proxy_info):
        try:
            stripped_url = proxy_info.split("://", 1)[-1]
            credentials, endpoint = stripped_url.split("@", 1)
            user_name, password = credentials.split(":", 1)
            ip, port = endpoint.split(":", 1)
            self.log(f"{self.green}Input IP Address: {self.white}{ip}")
            return {"user_name": user_name, "pass": password, "ip": ip, "port": port}
        except Exception as e:
            self.log(
                f"{self.red}Check proxy format: {self.white}http://user:pass@ip:port - {e}"
            )
            return None

base = Base()
