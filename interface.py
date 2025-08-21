import os
from scanner import scan_networks
from connector import connect, disconnect
from nm_control import enable_nm, disable_nm, status_nm

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def terminal_menu():
    while True:
        # limpa tela (Linux only)
        os.system("clear")

        # status rápido do NM
        nm_status = status_nm()
        if "UNMANAGED" in nm_status:
            color_status = GREEN
            alert_msg = ""
        else:
            color_status = RED
            alert_msg = f"{RED}⚠ Warning: wlan0 is still MANAGED by NetworkManager!{RESET}"

        # cabeçalho estilizado
        print(f"{CYAN}============================================================================={RESET}")
        print(f"{CYAN}                      Wi-Fi Manager RTL8XXXCU/GU/BU/CE/EU          {RESET}")
        print(f"{CYAN}                           Created by: ShuShuzinhuu  {RESET}")
        print(f"{CYAN}  (with a little help from ChatGPT and encouragement from mactavish011 😉)  {RESET}")
        print(f"{CYAN}============================================================================={RESET}")

        # alerta ou status
        if alert_msg:
            print(alert_msg + "\n")
        else:
            print(f" NetworkManager: {color_status}{nm_status}{RESET}\n")

        # opções
        print(f"{YELLOW}1.{RESET} Scan networks")
        print(f"{YELLOW}2.{RESET} Connect")
        print(f"{YELLOW}3.{RESET} Disconnect")
        print(f"{YELLOW}4.{RESET} Enable NetworkManager for wlan0")
        print(f"{YELLOW}5.{RESET} Disable NetworkManager for wlan0")
        print(f"{YELLOW}6.{RESET} Status NetworkManager")
        print(f"{YELLOW}7.{RESET} Exit\n")

        choice = input(f"{GREEN}Choose an option: {RESET}")

        if choice == "1":
            networks = scan_networks()
            if not networks:
                print(f"{RED}No networks found.{RESET}")
            else:
                print(f"\n{CYAN}Available Networks:{RESET}")
                for i, net in enumerate(networks):
                    print(f"{YELLOW}{i+1}.{RESET} {net['ssid']} ({net['signal']} dBm) {net['bars']}")
            input("\nPress ENTER to return...")
        
        elif choice == "2":
            ssid = input(f"{GREEN}SSID: {RESET}")
            password = input(f"{GREEN}Password: {RESET}")
            connect(ssid, password)
            input("\nPress ENTER to return...")
        
        elif choice == "3":
            disconnect()
            input("\nPress ENTER to return...")

        elif choice == "4":
            enable_nm()
            input("\nPress ENTER to return...")

        elif choice == "5":
            disable_nm()
            input("\nPress ENTER to return...")

        elif choice == "6":
            print(status_nm())
            input("\nPress ENTER to return...")

        elif choice == "7":
            print(f"{CYAN}Exiting...{RESET}")
            break

        else:
            print(f"{RED}Invalid option.{RESET}")
            input("\nPress ENTER to return...")

if __name__ == "__main__":
    terminal_menu()
