#!/usr/bin/env python

import sys
import subprocess
import tkinter as tk
from tkinter import ttk
import optparse
import re


# Set up GUI from instance of Tk
gui = tk.Tk()
gui.title('Kyle\'s MAC-Changer')

interface_name = ttk.Label(
    gui, text="Please provide the name of desired interface.")
interface_name.grid(row=0, column=0, sticky=tk.W)

interface = tk.StringVar()
interface_entry = ttk.Entry(gui, width=20, textvariable=interface)
interface_entry.grid(row=0, column=1)

mac = ttk.Label(gui, text="Please provide a new MAC address:")
mac.grid(row=1, column=0, sticky=tk.W)

mac = tk.StringVar()
mac_address = ttk.Entry(gui, width=20, textvariable=mac)
mac_address.grid(row=1, column=1)

parser = optparse.OptionParser()
parser.add_option(
    "--interface", help="Interface to change its MAC address[Ex. eth0]")
parser.add_option(
    "--mac", help="New MAC address you want to use[Alpha-num, 12 chars. Ex. 00:11:22[...]")
(options, arguments) = parser.parse_args()

# Run the change mac function with sanitized subprocess syntax


def change_mac():
    update_interface = interface.get()
    update_mac = mac.get()
    if not update_interface:
        sys.exit("Please provide a valid interface.")
    elif not update_mac:
        sys.exit("Please provide a valid MAC address.")
    elif update_interface == "lo":
        sys.exit("Cannot change this interface, invalid option.")
    else:
        print("[+] Changing mac address for " + update_interface + " to " + update_mac)
        subprocess.call(["ifconfig", update_interface, "down"])
        subprocess.call(["ifconfig", update_interface, "hw", "ether", update_mac])
        subprocess.call(["ifconfig", update_interface, "up"])
        sys.exit("MAC address successfully changed per specification.")


mac_button = ttk.Button(gui, text="Change MAC", command=change_mac)
mac_button.grid(row=4, column=1)
gui.mainloop()


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(
        r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(" [-] Could not read MAC address!")


current_mac = get_current_mac(interface)
print("Current MAC is equal to " + str(current_mac))

change_mac(interface, mac)
# Get current mac again..
current_mac = get_current_mac(interface)

# check if current mac is equal to requested MAC
if current_mac == mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did NOT get changed!")
