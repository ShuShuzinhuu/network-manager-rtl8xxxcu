import subprocess
import tempfile
import os
from getpass import getpass

def connect(ssid: str, password: str):
    """Connect to a Wi-Fi network using wpa_supplicant and dhclient."""
    wpa_conf = f"""
network={{
    ssid="{ssid}"
    psk="{password}"
}}
"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(wpa_conf.encode())
        temp_conf = f.name

    try:
        subprocess.run(["wpa_supplicant", "-B", "-i", "wlan0", "-c", temp_conf], check=True)
        subprocess.run(["dhclient", "wlan0"], check=True)
        print(f"✅ Connected to {ssid}")
    except Exception as e:
        print("❌ Error connecting:", e)
    finally:
        os.remove(temp_conf)

def disconnect():
    """Disconnect wlan0."""
    subprocess.run(["pkill", "-f", "wpa_supplicant"])
    subprocess.run(["dhclient", "-r", "wlan0"])
    print("✅ Disconnected from Wi-Fi.")
