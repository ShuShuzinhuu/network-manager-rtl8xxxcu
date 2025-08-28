import os
import sys
import asyncio
from interface import terminal_menu
from cdrom_check import detect_cdrom_adapters, switch_to_normal  # funções do módulo

def main():
    if os.geteuid() != 0:
        print("❌ This script must be run as root (sudo). Exiting...")
        sys.exit(1)

    try:
        # Detecta adaptadores em CD-ROM
        cdrom_adapters = detect_cdrom_adapters()
        if cdrom_adapters:
            print(f"⚠ {len(cdrom_adapters)} adapter(s) detected in CD-ROM mode!\n")
            for idx, (vendor, prod_cd, prod_normal) in enumerate(cdrom_adapters, 1):
                print(f"{idx}. Vendor: {vendor}, CD-ROM: {prod_cd}, Normal: {prod_normal}")

            # Solução interativa
            choice = input("\nDo you want to attempt switching all to normal mode? (y/n): ").strip().lower()
            if choice == "y":
                for vendor, prod_cd, prod_normal in cdrom_adapters:
                    switch_to_normal(vendor, prod_cd, prod_normal)
                print("\n✅ Attempted to switch adapters. Unplug/replug and re-run if needed.\n")
                asyncio.sleep(5)  
            else:
                print("\n❌ Please switch adapters to normal mode manually before continuing.\n")
                input("Press ENTER to exit...")
                sys.exit(0)

        # Se tudo estiver normal, inicia o menu
        terminal_menu()

    except KeyboardInterrupt:
        print("\n❌ Ctrl+C detected. Exiting gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    main()
