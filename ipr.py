from pyperclip import copy
mac= '58-b6-23-b9-5f-ed'
# get ip address using arp -a
import subprocess
ip_addresses = []
def get_ip_address(mac_address):
    try:
        # Run the arp command and capture the output
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        output = result.stdout
        # Parse the output to find the IP address for the given MAC address
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            ip_address = line.split()[0]
            device_mac_address = line.split()[1]
            if ip_address.startswith('192.168.1.'):
                ip_addresses.append(ip_address)
                print(ip_address, device_mac_address)
            if mac_address in line:
                # Extract the IP address from the line
                return ip_address
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
def resolve_ip():
    ip_address = get_ip_address(mac)
    if not ip_address:
        print(ip_addresses)
        for i in range(3,15):
            new_ip = f'192.168.1.{i}'
            print(new_ip)
            if new_ip not in ip_addresses:
                ping_result = subprocess.run(['ping', '-c', '1', new_ip], capture_output=True, text=True)
                if ping_result.returncode == 0:
                    print(f"IP Address: {new_ip}")
                    ip_address = get_ip_address(mac)
                    if ip_address:
                        break

    print(f"IP Address: {ip_address}")
    with open(r'C:\Users\smart\Documents\Modern-Activity-Tracker\ip.txt','w') as file:
        print(ip_address,file=file)

if __name__ == '__main__':
    resolve_ip()

