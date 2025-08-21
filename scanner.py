import subprocess
import re

def signal_to_bars(signal: int) -> str:
    """Convert dBm signal strength to 5-level bars."""
    if signal >= -50:
        return "[#####]"  # Excellent
    elif signal >= -60:
        return "[####_]"  # Good
    elif signal >= -70:
        return "[###__]"  # Medium
    elif signal >= -80:
        return "[##___]"  # Weak
    else:
        return "[#____]"  # Very weak

def scan_networks() -> list[dict]:
    """Scan Wi-Fi networks using iwlist and return list of dicts."""
    networks = []
    try:
        # Assume script already runs as root
        scan_output = subprocess.check_output(
            ["iwlist", "wlan0", "scan"], stderr=subprocess.DEVNULL
        ).decode()

        cells = scan_output.split("Cell ")
        for cell in cells[1:]:
            ssid_search = re.search(r'ESSID:"(.*)"', cell)
            if ssid_search:
                ssid = ssid_search.group(1)
                if not ssid or ssid == "<Hidden>":
                    continue  # Ignore hidden SSIDs

                signal_search = re.search(r'Signal level=(-?\d+) dBm', cell, re.IGNORECASE)
                signal = int(signal_search.group(1)) if signal_search else -100

                networks.append({
                    "ssid": ssid,
                    "signal": signal,
                    "bars": signal_to_bars(signal)
                })
    except subprocess.CalledProcessError:
        print("❌ Failed to scan networks. Are you root?")
    return networks
