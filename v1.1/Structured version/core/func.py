import os
import winreg
from core.constants import RESET, RED

def find_steam_workshop():
    """Finds Steam folder through registry and returns path to Scrap Mechanic workshop."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\Valve\\Steam") as key:
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
    except FileNotFoundError:
        steam_path = input("Steam not found in registry! Enter Steam path manually: ")
        if not os.path.exists(steam_path):
            print(f"{RED}Error: specified path does not exist!{RESET}")
            exit(1)
    
    workshop_path = os.path.join(steam_path, "steamapps", "workshop", "content", "387990")
    
    if not os.path.exists(workshop_path):
        workshop_path = input("Workshop path not found! Enter path manually: ")
        if not os.path.exists(workshop_path):
            print(f"{RED}Error: specified path does not exist!{RESET}")
            exit(1)
    
    return workshop_path
