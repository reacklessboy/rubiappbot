import time
import threading
from colorama import Fore, Style
from core.client import RubiClient

class MiningBot:
    def __init__(self, token, username, proxy=None, ip_info=None):
        self.token = token
        self.username = username
        self.proxy = proxy
        self.ip_info = ip_info or "Unknown"
        self.client = RubiClient(self.token, self.proxy)
        self.running = False
        self.mining_thread = None
        self.balance_thread = None
        self.token_refresh_thread = None
        self.last_ruby_block_swap_all = 0
        self.gems_gained = 0
        self.on_mining_success = None
        self.stop_event = threading.Event()

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    async def display_info(self):
        wallet_info = self.client.get_wallet_info()
        home_info = self.client.get_home_info()
        time_info = self.client.get_remaining_time()
        stock_info = self.client.get_stock_info()

        ruby_block_swap_all = 0
        exploit_speed = 0
        remaining_time = 0
        
        if home_info and 'data' in home_info and 'info' in home_info['data']:
            ruby_block_swap_all = home_info['data']['info'].get('ruby_block_swap_all', 0)
            exploit_speed = home_info['data']['info'].get('exploit_speed', 0)
        
        if time_info and 'data' in time_info:
            remaining_time = time_info['data'].get('time_remain', 0)
        
        return {
            'gems': ruby_block_swap_all,
            'mining_speed': exploit_speed,
            'time_remaining': remaining_time,
            'gems_gained': self.gems_gained
        }

    def update_real_time_balance(self):
        try:
            home_info = self.client.get_home_info()
            if home_info and 'data' in home_info and 'info' in home_info['data']:
                ruby_block_swap_all = home_info['data']['info'].get('ruby_block_swap_all', 0)
                difference = 0
                
                if self.last_ruby_block_swap_all > 0:
                    difference = ruby_block_swap_all - self.last_ruby_block_swap_all
                
                self.last_ruby_block_swap_all = ruby_block_swap_all
                return {'gems': ruby_block_swap_all, 'difference': difference}
            return None
        except Exception:
            return None

    def balance_updater(self):
        while not self.stop_event.is_set() and self.running:
            update = self.update_real_time_balance()
            if update and update['difference'] > 0:
                self.gems_gained += update['difference']
                print(f"\n{Fore.GREEN}[GEM] Miner {self.username}: {Fore.YELLOW}{update['gems']:.5f} | Change: +{Fore.YELLOW}{update['difference']:.5f}")
            time.sleep(30)

    def token_refresher(self):
        while not self.stop_event.is_set() and self.running:
            self.client.refresh_token()
            time.sleep(50 * 60)  # 50 minutes

    def mining_loop(self):
        # Run initial mining operation
        time.sleep(2)
        result = self.client.start_mining()
        if result and result.get('success'):
            print(f"\n{Fore.GREEN}[STARTED] Miner {Fore.WHITE}{self.username} has begun mining!")
        
        while not self.stop_event.is_set() and self.running:
            # Wait 5 minutes between mining operations
            time.sleep(5 * 60)
            
            if self.stop_event.is_set() or not self.running:
                break
                
            result = self.client.start_mining()
            if result and result.get('success'):
                home_info = self.client.get_home_info()
                gained = 0
                
                if home_info and 'data' in home_info and 'info' in home_info['data']:
                    new_gems = home_info['data']['info'].get('ruby_block_swap_all', 0)
                    gained = new_gems - self.last_ruby_block_swap_all
                    self.last_ruby_block_swap_all = new_gems
                    self.gems_gained += gained
                
                now = time.strftime("%H:%M:%S")
                print(f"\n{Fore.GREEN}[SUCCESS] Miner {Fore.WHITE}{self.username} completed a mining run! {now}")
                print(f"{Fore.GREEN}+ {Fore.YELLOW}{gained:.5f} gems added to your treasury")
            elif result:
                print(f"\n{Fore.RED}[FAILED] [{self.username}] Mining failed: {result.get('message', 'Unknown error')}")
            else:
                print(f"\n{Fore.RED}[FAILED] [{self.username}] Mining failed")

    def start_mining(self):
        if self.running:
            print(f"{Fore.YELLOW}[{self.username}] Mining bot is already running")
            return

        self.running = True
        self.stop_event.clear()
        print(f"{Fore.GREEN}[BOT] [{self.username}] Starting Rubi Click Mining Bot...")
        print(f"{Fore.BLUE}[IP] [{self.username}] Using IP: {Fore.YELLOW}{self.ip_info}")
        
        # Get initial info
        info = self.client.get_home_info()
        if info and 'data' in info and 'info' in info['data']:
            self.last_ruby_block_swap_all = info['data']['info'].get('ruby_block_swap_all', 0)
        
        # Start threads
        self.balance_thread = threading.Thread(target=self.balance_updater)
        self.balance_thread.daemon = True
        self.balance_thread.start()
        
        self.token_refresh_thread = threading.Thread(target=self.token_refresher)
        self.token_refresh_thread.daemon = True
        self.token_refresh_thread.start()
        
        self.mining_thread = threading.Thread(target=self.mining_loop)
        self.mining_thread.daemon = True
        self.mining_thread.start()

    def stop(self):
        if not self.running:
            print(f"{Fore.YELLOW}[{self.username}] Mining bot is not running")
            return

        self.running = False
        self.stop_event.set()
        print(f"{Fore.RED}[{self.username}] Mining bot stopped")