from flask import Flask, render_template, request, redirect, jsonify
import os
import socket
import concurrent.futures

app = Flask(__name__)

def scan_port(ip, port):
    """
    Attempts to connect to a given IP address and port to check if the port is open.
    return port number if open, otherwise return None.
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # timeout
        sock.settimeout(2)
        # connect_ex returns 0 if port is open
        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            return port
        return None
    except Exception as e:
        print(f"Error checking port {port} on {ip}: {e}")
        return None

# route server to the html page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for javascript to call and get the open ports
@app.route('/scan_ports', methods=['POST'])
def scan_ports():
    data = request.get_json()
    ip = data.get('ip')
    start_port = int(data.get('start_port', 1))
    end_port = int(data.get('end_port', 1024))

    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    open_ports = []

    #multithreading to scan multiple ports concurrently 
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}

        # check result after each thread completion
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port is not None:
                open_ports.append(port)

    open_ports.sort() 
    return jsonify({"ip": ip, "open_ports": open_ports})

if __name__ == '__main__':
    app.run(debug=True)