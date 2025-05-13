from colorama import Fore, Back, Style
from core.utils import clear_terminal

def display_miner_dashboard(bots):
    clear_terminal()
    
    total_gems = sum(bot.last_ruby_block_swap_all for bot in bots)
    
    print(f"{Back.MAGENTA}{Fore.WHITE}===== RUBI MINER BOT =====")
    print(f"{Fore.CYAN}Active Miners: {Fore.WHITE}{len(bots)} | Total Gems: {Fore.YELLOW}{total_gems:.5f}")
    print()
    
    for bot in bots:
        # Get bot info
        home_info = bot.client.get_home_info()
        time_info = bot.client.get_remaining_time()
        
        mining_speed = 0
        remaining_time = 0
        
        if home_info and 'data' in home_info and 'info' in home_info['data']:
            mining_speed = home_info['data']['info'].get('exploit_speed', 0)
        
        # Fix: Check that time_info['data'] is a dictionary before calling .get
        if time_info and isinstance(time_info.get('data'), dict):
            remaining_time = time_info['data'].get('time_remain', 0)
        else:
            remaining_time = 0
        
        print(f"{Fore.BLUE}Miner: {Fore.WHITE}{bot.username} | Location: {Fore.MAGENTA}{bot.ip_info}")
        print(f"{Fore.GREEN}Gems: {Fore.YELLOW}{bot.last_ruby_block_swap_all:.5f} (+{Fore.YELLOW}{bot.gems_gained:.5f})")
        print(f"{Fore.YELLOW}Mining Speed: {Fore.WHITE}{mining_speed}")
        print(f"{Fore.YELLOW}Time Remaining: {Fore.WHITE}{bot.format_time(remaining_time)}")
        print(f"{Fore.CYAN}[Mining in progress...]")
        print()
