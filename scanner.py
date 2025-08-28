import subprocess
import re

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def signal_to_bars(signal: int) -> str:
    if signal >= -50:
        return f"{GREEN}[#####]{RESET}"
    elif signal >= -60:
        return f"{GREEN}[####_]{RESET}"
    elif signal >= -70:
        return f"{YELLOW}[###__]{RESET}"
    elif signal >= -80:
        return f"{RED}[##___]{RESET}"
    else:
        return f"{RED}[#____]{RESET}"

def scan_networks() -> list[dict]:
    networks = []
    try:
        output = subprocess.check_output(
            ["iwlist", "wlan0", "scan"], stderr=subprocess.DEVNULL
        ).decode(errors="ignore")

        cells = output.split("Cell ")
        for cell in cells[1:]:
            ssid_search = re.search(r'ESSID:"(.*)"', cell)
            if not ssid_search:
                continue
            ssid = ssid_search.group(1)
            if not ssid or ssid == "<Hidden>":
                continue

            signal_search = re.search(r"Signal level=(-?\d+) dBm", cell, re.IGNORECASE)
            signal = int(signal_search.group(1)) if signal_search else -100

            wps_active = bool(re.search(r"\bWPS\b", cell, re.IGNORECASE))

            freq_search = re.search(r"Frequency:(\d+\.\d+) GHz", cell)
            freq = f"{freq_search.group(1)} GHz" if freq_search else "?"

            channel_search = re.search(r"Channel\s*(\d+)", cell)
            channel = channel_search.group(1) if channel_search else "?"

            networks.append({
                "ssid": ssid,
                "signal": signal,
                "bars": signal_to_bars(signal),
                "wps": f"{GREEN}✅ Active{RESET}" if wps_active else f"{RED}❌ Off{RESET}",
                "freq": freq,
                "channel": channel
            })

    except subprocess.CalledProcessError:
        print(f"{RED}❌ Failed to scan networks. Try Disconnect or Restart Network Control.{RESET}")

    return networks

def print_networks(networks: list[dict]):
    if not networks:
        print("No networks found.")
        return

    networks = sorted(networks, key=lambda x: x["signal"], reverse=True)

    print(f"\n{CYAN}{'SSID':<30}{'Signal':<12}{'dBm':<8}{'Freq':<10}{'Channel':<8}{'WPS':<10}{RESET}")
    print(f"{'-'*85}")

    for i, net in enumerate(networks, 1):
        print(f"{i}. {net['ssid']:<28}{net['bars']:<12}{net['signal']:<8}{net['freq']:<10}{net['channel']:<8}{net['wps']:<10}")

if __name__ == "__main__":
    nets = scan_networks()
    print_networks(nets)
