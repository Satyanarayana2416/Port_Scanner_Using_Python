# port_scanner.py
import socket
import threading
from queue import Queue

# Number of threads for scanning
THREADS = 100
# Queue for storing ports to be scanned
queue = Queue()
# List to store open ports
open_ports = []

# Function to scan individual ports
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)
        sock.close()
    except Exception as e:
        pass

# Worker function for threads
def threader(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

# Main function
def main():
    target = input("Enter IP address or domain to scan: ")
    try:
        ip = socket.gethostbyname(target)
        print(f"\n[~] Scanning target: {ip}...\n")
    except socket.gaierror:
        print("[-] Invalid hostname")
        return

    # Fill queue with port numbers (1 to 1024, common ports)
    for port in range(1, 1025):
        queue.put(port)

    # Start threads
    for _ in range(THREADS):
        t = threading.Thread(target=threader, args=(ip,))
        t.daemon = True
        t.start()

    queue.join()

    print("\nScan complete.")
    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(f" - {port}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
