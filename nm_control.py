import os
import subprocess
import sys
import time

CONF_PATH = "/etc/NetworkManager/conf.d/unmanaged-wlan0.conf"
DEVICE = "wlan0"

def check_root():
    if os.geteuid() != 0:
        print("❌ You need to run this script as root (sudo).")
        sys.exit(1)

def run_cmd(cmd: list) -> str:
    """Run a command and return stdout or stderr if it fails."""
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()

def disable_nm():
    """Disable NetworkManager management for wlan0."""
    check_root()
    content = "[keyfile]\nunmanaged-devices=interface-name:wlan0\n"
    try:
        with open(CONF_PATH, "w") as f:
            f.write(content)

        run_cmd(["nmcli", "device", "set", DEVICE, "managed", "no"])
        subprocess.run(["systemctl", "restart", "NetworkManager"], check=True)
        time.sleep(2)
        print("✅ NetworkManager set to NOT manage wlan0.")
    except Exception as e:
        print(f"❌ Error disabling NM: {e}")

def enable_nm():
    """Enable NetworkManager management for wlan0."""
    check_root()
    try:
        if os.path.exists(CONF_PATH):
            os.remove(CONF_PATH)

        run_cmd(["nmcli", "device", "set", DEVICE, "managed", "yes"])
        subprocess.run(["systemctl", "restart", "NetworkManager"], check=True)
        time.sleep(2)
        print("✅ NetworkManager set to manage wlan0.")
    except Exception as e:
        print(f"❌ Error enabling NM: {e}")

def status_nm() -> str:
    """Return the real NetworkManager status of wlan0."""
    output = run_cmd(["nmcli", "-t", "-f", "DEVICE,STATE", "device", "status"])
    for line in output.splitlines():
        if line.startswith(DEVICE):
            if "unmanaged" in line:
                return "🟢 wlan0 is UNMANAGED by NetworkManager."
            else:
                return "🔴 wlan0 is MANAGED by NetworkManager!"
    return "⚪ wlan0 not found. Check your adapter."
