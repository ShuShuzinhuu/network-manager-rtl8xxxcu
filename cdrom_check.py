import subprocess
import os
import shutil

# List of Realtek USB adapters that come in CD-ROM mode (vendor_id, product_id_cdrom, product_id_normal)
ADAPTERS = [
    ("0bda", "018a", "018b"),  # RTL8188CUS
    ("0bda", "0179", "017a"),  # RTL8188EU
    ("0bda", "081a", "081b"),  # RTL8812AU
    ("0bda", "1a2b", "1a2c"),  # RTL8188GU
    ("0bda", "8176", "8177"),  # RTL8192CU
    ("0bda", "b812", "b813"),  # RTL8811AU
    ("0bda", "8852", "8853"),  # RTL8852AE
]

def run_cmd(cmd: list) -> str:
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()

def detect_cdrom_adapters():
    """Detect connected Realtek USB adapters in CD-ROM mode."""
    lsusb_output = run_cmd(["lsusb"])
    cdrom_list = []
    for vendor, prod_cd, prod_normal in ADAPTERS:
        if f"{vendor}:{prod_cd}" in lsusb_output:
            cdrom_list.append((vendor, prod_cd, prod_normal))
    return cdrom_list

def switch_to_normal(vendor, prod_cd, prod_normal):
    """Switch a CD-ROM adapter to NIC (Wi-Fi) mode."""
    if not shutil.which("usb_modeswitch"):
        print("❌ usb_modeswitch not found. Install it first (sudo apt install usb-modeswitch).")
        return False

    print(f"\n⏳ Switching {vendor}:{prod_cd} -> NIC mode ({prod_normal}) ...")
    cmd = [
        "sudo", "usb_modeswitch",
        "-v", f"0x{vendor}", "-p", f"0x{prod_cd}", "-R"
    ]
    output = run_cmd(cmd)
    print(output)
    print("✅ If successful, unplug and replug the adapter, then check again.")
    return True

def interactive_cdrom_check():
    os.system("clear")
    print("🔹 Realtek USB Adapter Mode Check 🔹\n")
    cdrom_adapters = detect_cdrom_adapters()

    if not cdrom_adapters:
        print("✅ No adapters in CD-ROM mode detected. All normal!")
        return

    print(f"⚠ {len(cdrom_adapters)} adapter(s) detected in CD-ROM mode!\n")
    for idx, (vendor, prod_cd, prod_normal) in enumerate(cdrom_adapters, 1):
        print(f"{idx}. Vendor: {vendor}, CD-ROM: {prod_cd}, NIC: {prod_normal}")

    choice = input("\nDo you want to attempt switching all to NIC (Wi-Fi) mode? (y/n): ").strip().lower()
    if choice == "y":
        for vendor, prod_cd, prod_normal in cdrom_adapters:
            switch_to_normal(vendor, prod_cd, prod_normal)
    else:
        print("❌ No changes made. Exiting...")
