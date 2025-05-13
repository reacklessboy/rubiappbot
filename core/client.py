import os
import json
import requests
import uuid
import random
from datetime import datetime
from colorama import Fore, Style

from core.utils import generate_device_info, get_ip_info

BASE_URL = 'https://rubi.click/api'
HEADERS = {
    'User-Agent': 'okhttp/4.9.1',
    'Connection': 'Keep-Alive',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json',
    'lang': 'en',
    'driver-login': 'jwt',
    'app_version': '1.42'
}

EXPLOIT_STOCK_ID = 20

def login(username, password, proxy=None):
    try:
        if not username or not password:
            raise Exception('Username and password are required')
        
        ip_info = get_ip_info(proxy)
        print(f"{Fore.CYAN}Attempting to login with username: {Fore.YELLOW}{username} using proxy {Fore.MAGENTA}{ip_info}")
        
        device_info = generate_device_info()
        
        login_data = {
            "username": username,
            "password": password,
            **device_info
        }

        proxies = None
        if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
        
        response = requests.post(
            f"{BASE_URL}/login", 
            json=login_data, 
            headers=HEADERS,
            proxies=proxies
        )
        
        response_data = response.json()
        
        if response.status_code == 200 and 'access_token' in response_data:
            token = response_data['access_token']
            with open(f"token_{username}.txt", 'w') as f:
                f.write(token)
            print(f"{Fore.GREEN}Token refreshed for {username} and saved!")
            return {'token': token, 'ip_info': ip_info}
        else:
            error_msg = response_data.get('message', 'Unknown error')
            raise Exception(f"Login failed: {error_msg}")
            
    except Exception as e:
        print(f"{Fore.RED}Login failed: {str(e)}")
        raise

class RubiClient:
    def __init__(self, token, proxy=None):
        self.token = token
        self.proxy = proxy
        self.headers = {
            **HEADERS,
            'authorization': f'Bearer {token}'
        }
        
        self.proxies = None
        if proxy:
            self.proxies = {
                'http': proxy,
                'https': proxy
            }

    def get_config(self):
        try:
            response = requests.get(
                f"{BASE_URL}/config/all", 
                headers=self.headers,
                proxies=self.proxies
            )
            return response.json()
        except Exception as e:
            print(f"Error getting config: {str(e)}")
            return None

    def start_mining(self):
        try:
            response = requests.post(
                f"{BASE_URL}/exploit", 
                json={"exploit_stock_id": EXPLOIT_STOCK_ID},
                headers=self.headers,
                proxies=self.proxies
            )
            return response.json()
        except Exception as e:
            print(f"Error starting mining: {str(e)}")
            return None

    def get_stock_info(self):
        try:
            response = requests.get(
                f"{BASE_URL}/exploit/stock_v2", 
                headers=self.headers,
                proxies=self.proxies
            )
            return response.json()
        except Exception as e:
            print(f"Error getting stock info: {str(e)}")
            return None

    def get_remaining_time(self):
        try:
            response = requests.post(
                f"{BASE_URL}/exploit/time-remain", 
                json={},
                headers=self.headers,
                proxies=self.proxies
            )
            return response.json()
        except Exception as e:
            print(f"Error getting remaining time: {str(e)}")
            return None

    def get_home_info(self):
        try:
            response = requests.get(
                f"{BASE_URL}/home", 
                headers=self.headers,
                proxies=self.proxies
            )
            return response.json()
        except Exception as e:
            print(f"Error getting home info: {str(e)}")
            return None

    def get_wallet_info(self):
        try:
            headers = {
                **self.headers,
                'wallet-token': 'null',
                'wallet-code': 'null'
            }
            
            response = requests.get(
                f"{BASE_URL}/wallet/info", 
                headers=headers,
                proxies=self.proxies
            )
            return response.json()
        except Exception as e:
            print(f"Error getting wallet info: {str(e)}")
            return None

    def refresh_token(self):
        try:
            response = requests.post(
                f"{BASE_URL}/user/refresh", 
                json={},
                headers=self.headers,
                proxies=self.proxies
            )
            
            response_data = response.json()
            
            if 'access_token' in response_data:
                self.token = response_data['access_token']
                self.headers['authorization'] = f"Bearer {self.token}"
                
                with open(f"token.txt", 'w') as f:
                    f.write(self.token)
                print(f"{Fore.GREEN}Token refreshed and saved")
            
            return response_data
        except Exception as e:
            print(f"Error refreshing token: {str(e)}")
            return None

    def is_token_valid(self):
        try:
            response = self.get_home_info()
            return response and response.get('success') != False
        except Exception:
            return False