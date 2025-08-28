import subprocess
import os
from scanner import scan_networks
from connector import connect, disconnect
from nm_control import status_nm, restart_network_control

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CIANO = "\033[96m"
RESET = "\033[0m"

def terminal_menu():
    while True:
        os.system("clear")

        # NetworkManager status
        nm_status = status_nm()
        if "UNMANAGED" in nm_status:
            color_status = GREEN
            alert_msg = ""
        else:
            color_status = RED
            alert_msg = f"{RED}⚠ Warning: wlan0 is still MANAGED by NetworkManager!{RESET}"

        # Header
        print(f"{CIANO}============================================================================={RESET}")
        print(f"{CIANO}                      Wi-Fi Manager RTL8XXXCU/GU/BU/CE/EU          {RESET}")
        print(f"{CIANO}                           Created by: ShuShuzinhuu  {RESET}")
        print(f"{CIANO}  (with a little help from ChatGPT and encouragement from mactavish011 😉)  {RESET}")
        print(f"{CIANO}============================================================================={RESET}\n")

        # Alert or status
        if alert_msg:
            print(alert_msg + "\n")
        else:
            print(f" NetworkManager: {color_status}{nm_status}{RESET}\n")

        # Menu options
        print(f"{YELLOW}1.{RESET} Scan & Connect")
        print(f"{YELLOW}2.{RESET} Disconnect")
        print(f"{YELLOW}3.{RESET} Release DHCP (Wlan0 connected but no internet)")
        print(f"{YELLOW}4.{RESET} Restart Network Control (leave wlan0 unmanaged)")
        print(f"{YELLOW}5.{RESET} Status NetworkManager")
        print(f"{YELLOW}6.{RESET} Exit\n")

        choice = input(f"{GREEN}Choose an option: {RESET}")

        if choice == "1":
            interactive_scan_connect()
        
        elif choice == "2":
            disconnect()
            input("\nPress ENTER to return...")

        elif choice == "3":
            subprocess.run(["dhclient", "wlan0"], check=True)
            print(f"{GREEN}✅ DHCP released on wlan0{RESET}")
            input("Press ENTER to return...")

        elif choice == "4":
            restart_network_control()
            input("\nPress ENTER to return...")

        elif choice == "5":
            print(status_nm())
            input("\nPress ENTER to return...")

        elif choice == "6":
            print(f"{CIANO}Exiting...{RESET}")
            break

        else:
            print(f"{RED}Invalid option.{RESET}")
            input("\nPress ENTER to return...")

# ====================== Interactive Scan & Connect ======================

def interactive_scan_connect():
    networks = scan_networks()
    if not networks:
        print(f"{RED}No networks found.{RESET}")
        input("\nPress ENTER to return...")
        return

    # Sort networks by signal descending
    networks = sorted(networks, key=lambda x: x["signal"], reverse=True)

    # Table header
    print(f"\n{CIANO}{'No.':<4}{'SSID':<30}{'Bars':<10}{'Signal(dBm)':<12}{'Freq':<10}{'Channel':<8}{'WPS':<10}{RESET}")
    print(f"{'-'*85}")

    for i, net in enumerate(networks, 1):
        ssid = net['ssid'][:28]  # truncate long SSIDs
        print(f"{i:<4}{ssid:<30}{net['bars']:<10}{net['signal']:<12}{net['freq']:<10}{net['channel']:<8}{net['wps']:<10}")

    # User selection
    while True:
        selection = input(f"\nSelect a network to connect (0 to cancel): ")
        if not selection.isdigit():
            print(f"{RED}Invalid input!{RESET}")
            continue
        selection = int(selection)
        if selection == 0:
            break
        if 1 <= selection <= len(networks):
            net = networks[selection - 1]
            password = input(f"{GREEN}Enter password for '{net['ssid']}': {RESET}")
            connect(net['ssid'], password)
            input("\nPress ENTER to return...")
            break
        else:
            print(f"{RED}Invalid number!{RESET}")

if __name__ == "__main__":
    terminal_menu()
