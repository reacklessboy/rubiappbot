import os
import uuid
import random
import requests
import json
from colorama import Fore, Style

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_device_info():
   manufacturers = [
       'Samsung', 'Xiaomi', 'OnePlus', 'OPPO', 'Vivo', 'Realme', 'Huawei', 'Google', 'Nokia', 
       'Motorola', 'Sony', 'LG', 'Asus', 'Lenovo', 'TCL', 'ZTE', 'Sharp', 'BlackBerry', 'Honor',
       'Nothing', 'Infinix', 'Poco', 'iQOO', 'Tecno', 'Micromax'
   ]
   
   device_models = [
       'SM-A505F', 'SM-G973F', 'SM-N975F', 'SM-S908B', 'SM-F926B', 'SM-A536B', 'SM-M526B',
       'SM-A735F', 'SM-G990B', 'SM-S901B', 'SM-F711B', 'SM-A326B', 'SM-T970', 'SM-G781B',
       'Redmi Note 9', 'Mi 11 Ultra', 'Poco X3 Pro', 'Redmi 10', 'Mi 11T Pro', 'Redmi Note 11',
       'Mi 10T Lite', 'Redmi 9A', 'Poco F3', 'Redmi K40 Pro', 'Mi Mix 4', 'Redmi Note 10 Pro',
       'OnePlus 9 Pro', 'OnePlus Nord 2', 'OnePlus 10T', 'OnePlus 8T', 'OnePlus Nord CE 2',
       'OnePlus 9R', 'OnePlus Ace', 'OnePlus Nord N200', 'OnePlus 10 Pro', 'OnePlus 7T Pro',
       'Find X5 Pro', 'Reno 7 Pro', 'A96', 'F19 Pro', 'Find N', 'Reno 6', 'F21 Pro', 'A74',
       'Find X3 Neo', 'Reno 5 Lite', 'A54', 'F17', 'Reno 4 Pro',
       'X80 Pro', 'V23 Pro', 'Y75', 'X70 Pro+', 'V21', 'Y21s', 'X60 Pro', 'V20', 'Y33s',
       'GT 2 Pro', 'GT Neo 3', '9 Pro+', 'GT Master', '8i', 'C35', 'GT Neo 2', '9i', 'Narzo 50',
       'P50 Pro', 'Nova 9', 'Mate 40 Pro', 'P40 Lite', 'Mate Xs 2', 'Nova 8i', 'Y9a', 'MatePad 11',
       'Pixel 7 Pro', 'Pixel 6a', 'Pixel 5', 'Pixel 4 XL', 'Pixel 6 Pro', 'Pixel 4a', 'Pixel 3a',
       'Nokia X20', 'Motorola Edge 30', 'Sony Xperia 1 IV', 'LG Velvet', 'Asus Zenfone 8',
       'Lenovo Legion Phone Duel 2', 'TCL 30', 'ZTE Axon 40 Ultra', 'Nothing Phone 1'
   ]
   
   device_names = [
       'samsung-a50', 'samsung-s10', 'samsung-note10', 'samsung-s22ultra', 'samsung-zfold3', 
       'samsung-a53', 'samsung-m52', 'samsung-a73', 'samsung-s21fe', 'samsung-s22', 
       'samsung-zflip3', 'samsung-a32', 'samsung-tabs7', 'samsung-s20fe',
       'xiaomi-redminote9', 'xiaomi-mi11ultra', 'xiaomi-pocox3pro', 'xiaomi-redmi10', 
       'xiaomi-mi11tpro', 'xiaomi-redminote11', 'xiaomi-mi10tlite', 'xiaomi-redmi9a', 
       'xiaomi-pocof3', 'xiaomi-redmik40pro', 'xiaomi-mimix4', 'xiaomi-redminote10pro',
       'oneplus-9pro', 'oneplus-nord2', 'oneplus-10t', 'oneplus-8t', 'oneplus-nordce2', 
       'oneplus-9r', 'oneplus-ace', 'oneplus-nordn200', 'oneplus-10pro', 'oneplus-7tpro',
       'oppo-findx5pro', 'oppo-reno7pro', 'oppo-a96', 'oppo-f19pro', 'oppo-findn', 
       'oppo-reno6', 'oppo-f21pro', 'oppo-a74', 'oppo-findx3neo', 'oppo-reno5lite', 
       'oppo-a54', 'oppo-f17', 'oppo-reno4pro',
       'vivo-x80pro', 'vivo-v23pro', 'vivo-y75', 'vivo-x70proplus', 'vivo-v21', 'vivo-y21s', 
       'vivo-x60pro', 'vivo-v20', 'vivo-y33s',
       'realme-gt2pro', 'realme-gtneo3', 'realme-9proplus', 'realme-gtmaster', 'realme-8i', 
       'realme-c35', 'realme-gtneo2', 'realme-9i', 'realme-narzo50',
       'huawei-p50pro', 'huawei-nova9', 'huawei-mate40pro', 'huawei-p40lite', 'huawei-matexs2', 
       'huawei-nova8i', 'huawei-y9a', 'huawei-matepad11',
       'google-pixel7pro', 'google-pixel6a', 'google-pixel5', 'google-pixel4xl', 
       'google-pixel6pro', 'google-pixel4a', 'google-pixel3a',
       'nokia-x20', 'motorola-edge30', 'sony-xperia1iv', 'lg-velvet', 'asus-zenfone8', 
       'lenovo-legion2', 'tcl-30', 'zte-axon40ultra', 'nothing-phone1'
   ]
   
   android_versions = ['10', '11', '12', '13']
   
   random_index = random.randint(0, len(manufacturers) - 1)
   random_device_id = uuid.uuid4().hex[:16]
   random_push_token = str(uuid.uuid4())
   
   return {
       "device_push_token": random_push_token,
       "device_os": "android",
       "device_id": random_device_id,
       "device_name": device_names[random_index],
       "device_model": device_models[random_index],
       "device_branch": manufacturers[random_index],
       "device_os_version": random.choice(android_versions),
       "device_manufacturer": manufacturers[random_index]
   }

def get_ip_info(proxy):
    try:
        ip = "Direct Connection"
        if proxy:
            # Extract IP from proxy string (assuming format http://username:password@ip:port or http://ip:port)
            import re
            match = re.search(r'//(?:.*@)?([^:]+):', proxy)
            if match and match.group(1):
                ip = match.group(1)
        
        # Try to get more info about the IP
        try:
            if ip != "Direct Connection":
                response = requests.get(f"http://ip-api.com/json/{ip}")
                if response.status_code == 200:
                    data = response.json()
                    if 'country' in data:
                        return f"{ip} ({data['country']})"
        except Exception:
            # If IP lookup fails, just return the IP
            pass
        
        return ip
    except Exception:
        return "Unknown"

def read_accounts_from_file():
    if not os.path.exists('accounts.txt'):
        raise Exception('accounts.txt file not found')

    with open('accounts.txt', 'r') as f:
        accounts = f.read().splitlines()
    
    result = []
    for line in accounts:
        line = line.strip()
        if line:
            username, password = line.split(':', 1)
            result.append({
                'username': username.strip(),
                'password': password.strip()
            })
    
    return result

def read_proxies_from_file():
    if not os.path.exists('proxies.txt'):
        print(f"{Fore.YELLOW}proxies.txt file not found, continuing without proxies")
        return []

    with open('proxies.txt', 'r') as f:
        proxies = f.read().splitlines()
    
    result = []
    for line in proxies:
        line = line.strip()
        if line:
            if '://' not in line:
                line = f"http://{line}"
            result.append(line)
    
    print(f"{Fore.CYAN}Loaded {Fore.WHITE}{len(result)} proxies from proxies.txt")
    return result