# network-manager-rtl8xxxcu (Arch Linux)

**Wi‑Fi Manager for USB RTL8XXXCU / RTL8188GU adapters**

This tool simplifies manual Wi‑Fi connections on cheap USB Realtek adapters (e.g. RTL8188GU / RTL8XXXCU) by making `wlan0` unmanaged by NetworkManager and handling connections directly with **iw**, **wpa\_supplicant**, and **dhclient**.

> Created by: ShuShuzinhuu & mactavish011
> (with a little help from ChatGPT)

---

## Important — Arch Linux only

This repository and README are intended for **Arch Linux** (and Arch-based) systems. The installation and dependency instructions use `pacman`. If you want support for other distributions, request it and a separate README will be provided.

---

## ⚠️ Warnings

* **Run as root** (`sudo`) — the scripts require root privileges to enable/disable NetworkManager and to run `wpa_supplicant`/`dhclient`.
* Tested primarily with **RTL8188GU / RTL8XXXCU USB adapters**.
* Hidden/closed SSIDs are ignored by the scanner.
* NetworkManager **must** be installed to use the enable/disable (managed/unmanaged) functionality (`nmcli` is used).
* For debugging, check `dmesg`, `rfkill`, and `nmcli device status`.

---

## Features

* Toggle NetworkManager control for `wlan0` (managed ↔ unmanaged).
* Scan Wi‑Fi networks (SSID + signal strength).
* Connect to networks with SSID + password via `wpa_supplicant` + `dhclient`.
* Quick disconnect (stop `wpa_supplicant` and release DHCP).
* Interactive terminal menu (TUI) for the common operations.

---

## Dependencies (Arch Linux)

```bash
sudo pacman -Syu --needed python-pip python-dbus python-psutil iw wpa_supplicant dhclient networkmanager usb_modeswitch git
```

Notes:

* The script uses `iw`, `wpa_supplicant`, and `dhclient`.
* `nmcli` (from `networkmanager`) is required to change the managed/unmanaged state of the interface.
* The project contains `cdrom_check.py` which attempts to detect Realtek USB adapters that present themselves as a CD-ROM device and uses `usb_modeswitch` to flip them into their network (USB NIC) mode. `usb_modeswitch` is therefore a required dependency on systems where this is needed.

---

## Install & run

```bash
# clone the repository
git clone https://github.com/ShuShuzinhuu/network-manager-rtl8xxxcu.git
cd network-manager-rtl8xxxcu

# run the Wi‑Fi manager (as root)
sudo python3 main.py
```

The program launches a terminal menu with options to scan, connect, disconnect, toggle NetworkManager control, show status, and exit.

---

## Implementation notes (from code review)

* **Interface name is hardcoded to `wlan0`** in multiple modules (e.g. `nm_control.py` uses `DEVICE = "wlan0"`). Update the constant in the code or implement an autodetect if your system uses a different interface name (e.g. `wlp2s0`).

* `nm_control.py` persists the unmanaged status by writing a file under `/etc/NetworkManager/conf.d/` (for example `/etc/NetworkManager/conf.d/unmanaged-wlan0.conf`) — be aware this will survive reboots.

* `cdrom_check.py` detects Realtek adapters that present as a CD-ROM and invokes `usb_modeswitch` to switch the device into its network mode. The original helper message in the code referenced `apt` for installing `usb_modeswitch`; that should be changed to `pacman` on Arch systems (the README includes the correct Arch package name).

---

## Usage (menu options)

1. **Scan networks** — lists visible networks with signal strength and SSID.
2. **Connect to Wi‑Fi** — enter SSID and password; script launches `wpa_supplicant` and runs `dhclient`.
3. **Disconnect** — stops `wpa_supplicant` and releases DHCP lease.
4. **Enable NetworkManager** — mark `wlan0` as managed by NetworkManager (restores automatic control).
5. **Disable NetworkManager** — set `wlan0` as unmanaged to allow manual control.
6. **Check status** — show if `wlan0` exists and whether it is managed by NetworkManager.
7. **Exit** — quit the menu.

---

## Quick manual commands (for debugging)

```bash
# scan
sudo iw dev wlan0 scan | less

# create wpa config and connect
wpa_passphrase "SSID" "PASSWORD" > /tmp/wpa.conf
sudo wpa_supplicant -B -i wlan0 -c /tmp/wpa.conf  # -B runs in background
sudo dhclient wlan0

# disconnect
sudo pkill wpa_supplicant
sudo dhclient -r wlan0

# toggle NetworkManager control
sudo nmcli device set wlan0 managed no   # unmanaged (manual control)
sudo nmcli device set wlan0 managed yes  # managed (NetworkManager)
```

> If your Wi‑Fi device uses a different name (e.g. `wlp2s0`), update the script or create a wrapper; the code assumes `wlan0` by default.

---

## Status symbols (menu)

* 🟢 `wlan0` **UNMANAGED** — ready for manual control
* 🔴 `wlan0` **MANAGED** — cannot be manually controlled by the script while managed
* ⚪ `wlan0` **not found** — check USB connection and drivers

---

## Troubleshooting checklist

* `dmesg | tail` — kernel messages about the adapter (firmware/driver errors).
* `lsusb` — confirm the adapter is detected on the USB bus.
* `ip link` / `ip addr` — check for `wlan0` presence.
* `rfkill list` — ensure the radio is not blocked (`sudo rfkill unblock all`).
* `nmcli device status` — verify NetworkManager state.
* `ps aux | grep wpa_supplicant` — ensure no conflicting instances are running.
* Check which kernel module is loaded (`lsmod | grep rtl`) — some Realtek devices have alternate modules (e.g. `rtl8xxxu`, `rtl8188eu`).

---

## Suggestions & TODO (ideas for contributions)

* Add CLI arguments (e.g. `--scan`, `--connect "SSID" "PASS"`) for non‑interactive use.
* Add automatic detection of the wireless interface name instead of assuming `wlan0`.
* Implement auto‑reconnect and retry policies.
* Add detailed logging to a file for easier debugging.

---

## Contributing

Open an issue or send a pull request. Please include logs or `dmesg` output when reporting adapter/driver issues.

---

## License & credits

License: **MIT**.

Authors: ShuShuzinhuu & mactavish011.

(Repository adapted for Arch Linux usage.)
