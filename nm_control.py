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
    """Restart NetworkManager and leave wlan0 as UNMANAGED."""
    check_root()
    content = "[keyfile]\nunmanaged-devices=interface-name:wlan0\n"
    try:
        with open(CONF_PATH, "w") as f:
            f.write(content)

        print("⏳ Restarting NetworkManager and leaving wlan0 unmanaged...")

        run_cmd(["nmcli", "device", "set", DEVICE, "managed", "no"])

        subprocess.run(["systemctl", "stop", "NetworkManager"], check=True)
        time.sleep(1)
        subprocess.run(["systemctl", "start", "NetworkManager"], check=True)
        time.sleep(2)

        run_cmd(["nmcli", "device", "set", DEVICE, "managed", "no"])

        print("✅ NetworkManager restarted and wlan0 remains UNMANAGED.")
    except Exception as e:
        print(f"❌ Error disabling NM: {e}")

def enable_nm():
    """Enable NetworkManager management for wlan0 normally."""
    check_root()
    try:
        if os.path.exists(CONF_PATH):
            os.remove(CONF_PATH)

        print("⏳ Enabling wlan0 management...")

        run_cmd(["nmcli", "device", "set", DEVICE, "managed", "yes"])

        subprocess.run(["systemctl", "stop", "NetworkManager"], check=True)
        time.sleep(1)
        subprocess.run(["systemctl", "start", "NetworkManager"], check=True)
        time.sleep(2)

        print("✅ NetworkManager is now managing wlan0.")
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

def restart_network_control():
    """Restart NetworkManager, disconnect any active network, and leave wlan0 UNMANAGED."""
    check_root()
    print("⏳ Disconnecting active network and restarting NetworkManager...")

    try:
        # Kill any wpa_supplicant sessions
        subprocess.run(["pkill", "-f", "wpa_supplicant"], check=False)
        # Release DHCP lease
        subprocess.run(["dhclient", "-r", DEVICE], check=False)

        # Restart NetworkManager
        subprocess.run(["systemctl", "stop", "NetworkManager"], check=True)
        time.sleep(1)
        subprocess.run(["systemctl", "start", "NetworkManager"], check=True)
        time.sleep(2)

        # Disconnect wlan0 from any network
        run_cmd(["nmcli", "device", "disconnect", DEVICE])
        # Ensure wlan0 unmanaged
        run_cmd(["nmcli", "device", "set", DEVICE, "managed", "no"])

        # Write config to persist unmanaged
        with open(CONF_PATH, "w") as f:
            f.write("[keyfile]\nunmanaged-devices=interface-name:wlan0\n")

        print("✅ NetworkManager restarted. wlan0 is UNMANAGED and disconnected from all networks.")
    except Exception as e:
        print(f"❌ Error restarting NetworkManager: {e}")
