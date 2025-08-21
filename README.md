# wlan network-manager-rtl8xxxcu

**Wi-Fi Manager** for **USB RTL8XXXCU/GU adapters**.  
This tool simplifies manual Wi-Fi connections on cheap USB adapters (like the ones sold on AliExpress), by blocking `NetworkManager` from managing `wlan0` and handling connections manually using **iw, wpa_supplicant, and dhclient**.

> Created by: ShuShuzinhuu & mactavish011  
> (with a little help from ChatGPT 😉)

---
## ⚠️ Alert

* Must run as root (`sudo`) to enable/disable NM and use wpa\_supplicant
* Tested primarily with USB RTL8188GU adapters
* Hidden SSIDs are ignored
* NetworkManager must be installed for enable/disable functionality
* For issues, check `dmesg` or run `nmcli device status`

## ✨ Features

- Enable/disable `NetworkManager` control for `wlan0`  
- Scan Wi-Fi networks  
- Connect to Wi-Fi manually (SSID + password)  
- Quick disconnect  
- Interactive terminal menu (TUI)  
- Designed for **RTL8188GU / RTL8XXXCU USB adapters**  

---

## 🛠 Dependencies

### Arch Linux
```bash
# Install all required system and Python packages
sudo pacman -S python-pip python-dbus python-psutil iw wpa_supplicant dhclient git

# Clone the repository
git clone https://github.com/ShuShuzinhuu/network-manager-rtl8xxxcu.git
cd network-manager-rtl8xxxcu

# Run the Wi-Fi manager
sudo python3 main.py
````

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install python3-pip python3-dbus python3-psutil iw wpa_supplicant dhclient git
git clone https://github.com/ShuShuzinhuu/network-manager-rtl8xxxcu.git
cd network-manager-rtl8xxxcu
sudo python3 main.py
```

### Fedora / RHEL

```bash
sudo dnf install python3-pip python3-dbus python3-psutil iw wpa_supplicant dhclient git NetworkManager
git clone https://github.com/ShuShuzinhuu/network-manager-rtl8xxxcu.git
cd network-manager-rtl8xxxcu
sudo python3 main.py
```

---

## Usage

1. **Scan networks**: option 1 → lists available networks with signal strength
2. **Connect to Wi-Fi**: option 2 → enter SSID and password
3. **Disconnect**: option 3 → stops wpa\_supplicant and releases DHCP
4. **Enable NetworkManager**: option 4 → restores NM management for wlan0
5. **Disable NetworkManager**: option 5 → stops NM from managing wlan0
6. **Check status**: option 6 → shows if wlan0 is managed or unmanaged
7. **Exit**: option 7 → exits the menu

---

## Status Symbols

* 🟢 wlan0 is UNMANAGED by NetworkManager → Ready for manual control
* 🔴 wlan0 is MANAGED by NetworkManager → Warning! Script cannot manually control
* ⚪ wlan0 not found → Check your USB adapter connection

---



