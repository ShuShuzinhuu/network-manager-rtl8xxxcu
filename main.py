import os
import sys
from interface import terminal_menu

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("❌ This script must be run as root (sudo). Exiting...")
        sys.exit(1)
    
    terminal_menu()
