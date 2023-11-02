import socket
import threading
import os
import subprocess

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    
    # Extract the requested file path from the HTTP request
    request_lines = request_data.split('\n')
    request_line = request_lines[0]
    parts = request_line.split()
    if len(parts) > 1:
        file_path = parts[1]
    else:
        client_socket.close()
        response = "HTTP/1.1 400 Bad Request\r\n\r\n<h1>Bad Request<h1>"
        return
    print(f'print file path: {file_path}')
    
      # Map the requested path to the local file system
    root_dir = '.'
    file_path = file_path.lstrip('/')
    requested_file = os.path.join(root_dir, file_path)

    if os.path.exists(requested_file) and os.path.isfile(requested_file):
        # Read the file and prepare the HTTP response
        with open(requested_file, 'rb') as f:
            content = f.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: text/html\r\n\r\n{content.decode('utf-8')}"
    else:
        # File not found, send a 404 response
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>File not found<h1>"

    # Send the response back to the client
    client_socket.sendall(response.encode())
    client_socket.close()
    
    

def main():

    port = 6789

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output = subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()
    host = output.split()[0]
    print(f"Proxy_host: {host}")
    server.bind((host, port))
    server.listen(5)  # Listen for up to 5 client connections

    print(f"[*] Listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from client {addr[0]}:{addr[1]}")
        
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
