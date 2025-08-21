# rtl8xxxcu-eu-wlan-manager

**Wi-Fi Manager** for **USB RTL8XXXCU/GU adapters**.  
This tool simplifies manual Wi-Fi connections on cheap USB adapters (like the ones sold on AliExpress), by blocking `NetworkManager` from managing `wlan0` and handling connections manually using **iw, wpa_supplicant, and dhclient**.

> Created by: ShuShuzinhuu & mactavish011  
> (with a little help from ChatGPT 😉)

---

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
