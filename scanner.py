import socket
import threading
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

# Argument Parser
parser = argparse.ArgumentParser(description="Advanced Multi-threaded Port Scanner")
parser.add_argument("-t", "--target", required=True, help="Target IP address")
parser.add_argument("-sp", "--startport", type=int, required=True, help="Start Port")
parser.add_argument("-ep", "--endport", type=int, required=True, help="End Port")

args = parser.parse_args()

target = args.target
start_port = args.startport
end_port = args.endport

print(Fore.CYAN + "=== Advanced Port Scanner ===")
print(Fore.YELLOW + f"\nScanning {target}...\n")

lock = threading.Lock()
open_ports = []

def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No Banner"

            with lock:
                print(Fore.GREEN + f"[OPEN] Port {port} | Service Info: {banner}")
                open_ports.append((port, banner))

        sock.close()

    except:
        pass

threads = []

for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Save Results to File
with open("scan_report.txt", "w") as file:
    file.write(f"Scan Results for {target}\n\n")
    for port, banner in open_ports:
        file.write(f"Port {port} | Service Info: {banner}\n")

print(Fore.CYAN + "\nScan Completed!")
print(Fore.CYAN + "Results saved to scan_report.txt")