import os
import sys
import time
import signal
import threading
from colorama import init, Fore, Back, Style

from core.utils import clear_terminal, read_accounts_from_file, read_proxies_from_file
from core.client import login
from core.miner import MiningBot
from core.dashboard import display_miner_dashboard

# Initialize colorama
init(autoreset=True)

bots = []
should_exit = False

def signal_handler(sig, frame):
    global should_exit
    print(f"\n{Fore.YELLOW}Stopping all mining bots...")
    should_exit = True
    for bot in bots:
        bot.stop()
    sys.exit(0)

def main():
    global bots
    
    clear_terminal()
    print(f"{Back.BLUE}{Fore.WHITE}===== RUBI CLICK MULTI-ACCOUNT MINING BOT =====")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop the bot at any time\n")

    accounts = read_accounts_from_file()
    proxies = read_proxies_from_file()
    print(f"{Fore.CYAN}Found {Fore.WHITE}{len(accounts)} accounts in accounts.txt")

    for i, account in enumerate(accounts):
        username = account['username']
        password = account['password']
        proxy = proxies[i % len(proxies)] if proxies else None
        
        # Always refresh token on start
        try:
            login_result = login(username, password, proxy)
            token = login_result['token']
            ip_info = login_result['ip_info']
        except Exception as e:
            print(f"{Fore.RED}[{username}] Login failed: {str(e)}. Skipping this account.")
            continue
        
        print(f"{Back.MAGENTA}{Fore.WHITE}==========Accounts==========")
        bot = MiningBot(token, username, proxy, ip_info)
        bots.append(bot)
        bot.start_mining()

    if not bots:
        print(f"{Fore.RED}No valid accounts to mine with. Exiting.")
        sys.exit(1)

    # Set up the dashboard refresh
    threading.Thread(target=dashboard_updater, daemon=True).start()

def dashboard_updater():
    global bots, should_exit
    
    # Display initial dashboard after a short delay
    time.sleep(5)
    display_miner_dashboard(bots)
    
    while not should_exit:
        time.sleep(60)
        if not should_exit:
            display_miner_dashboard(bots)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
    
    try:
        # Keep the main thread alive
        while not should_exit:
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Add a pause before closing when running in a GUI
    input("Press Enter to exit...")
