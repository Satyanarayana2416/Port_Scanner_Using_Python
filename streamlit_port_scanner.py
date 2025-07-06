import socket
import threading
from queue import Queue
import streamlit as st

# Constants
THREADS = 100
PORT_RANGE = range(1, 1025)
queue = Queue()
open_ports = []

# Function to scan a single port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass 

# Worker thread
def threader(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

# Streamlit UI
st.title("🔍 Port Scanner")
st.markdown("Enter a domain or IP address to scan for open ports (1–1024).")

target = st.text_input("Target Domain or IP", placeholder="example.com")
start_scan = st.button("Start Scan")

if start_scan and target:
    open_ports.clear()
    try:
        ip = socket.gethostbyname(target)
        st.success(f"Resolved IP: {ip}")
    except socket.gaierror:
        st.error("❌ Invalid domain or IP.")
    else:
        # Fill queue
        for port in PORT_RANGE:
            queue.put(port)

        with st.spinner("Scanning..."):
            for _ in range(THREADS):
                t = threading.Thread(target=threader, args=(ip,))
                t.daemon = True
                t.start()

            queue.join()

        st.success("Scan Complete ✅")
        if open_ports:
            st.write("### 🟢 Open Ports")
            st.table([{"Port": port} for port in sorted(open_ports)])
        else:
            st.warning("No open ports found.")
