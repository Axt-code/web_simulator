
import socket
import threading
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl
import subprocess

# Define the proxy's listening address and port
output = subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()
proxy_host = output.split()[0]
proxy_port = 8090


def modify_header(header, status_code):
    # Add the additional lines to the header
    header += "\r\n"
    header += f"Proxy host: {proxy_host}"

    return header
        
def handle_client(client_socket):
    request = client_socket.recv(4096).decode('utf-8')

    print("Request: "+ request)

    headers = request.split("\r\n")
    host_header = [header for header in headers if header.startswith("Host:")]
        
    if host_header:
        host_port = host_header[0].split(": ")[1].split(":")
        host = host_port[0]
        port_str = host_port[1] if len(host_port) > 1 else 80  # Default to port 80 if no port is specified
        
    
    if port_str:  # Check if port_str is a valid integer
        port = int(port_str)
        print(f"host: {host}")
        print(f"port: {port}")
    else:
        print("Host header not found in the request.")

    if host_header:
        # Extract the hostname from the Host header
        url = (host_header[0].split(" ")[1].split(":")[0])
        
    print(f"URL: {url}")
        
    if not host:
        print("Error: Invalid URL")
        return
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if(port == 443):
            context = ssl.create_default_context()
            server_socket = context.wrap_socket(server_socket, server_hostname=host)
            
            
    server_socket.connect((host, port))
    
    # Send the request to the server or proxy
    server_socket.send(request.encode())
    
    print("Request send")

    byteResponse = b""
    
    server_socket.settimeout(20)
    
    try:
        while True:
            response_chunk = server_socket.recv(4096)
            if not response_chunk:
                break
            byteResponse += response_chunk
    except:
        pass
    
    
    print("Closing Connection with server")
    print()
    
    server_socket.close()
    
    
     # Process the HTTP response
    response_parts = byteResponse.split(b'\r\n\r\n')
    
    status_code=""
    
    if len(response_parts) == 2:
        headers, script_data = response_parts
        status_line, *header_lines = headers.decode('utf-8').split('\r\n')
        status_code = status_line.split()[1].encode('utf-8')
        if status_code != b'200':
            error_message = f"Error: Received status code {status_code}"
            print(error_message)
            print()
            client_socket.send(error_message.encode())
            
    print(f"status code: {status_code.decode('utf-8')}\n")
    
    # modified_headers = modify_header(headers.decode('utf-8'), status_code.decode('utf-8'))

    # print(f"Modified header: {modified_headers}")
 
    # Create the modified response by combining the modified headers and the original script_data
    # modified_response = f"{modified_headers}\r\n{script_data.decode('utf-8')}"
    # print(modified_response.encode('utf-8'))

    # Send the modified response to the client as bytes
    client_socket.send(byteResponse)
        
    
    print("Closing Connection with client")
    print()
    
    # Close both sockets
    client_socket.close()


def main():
    # Create a listening socket
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Proxy_host: {proxy_host}")
    server.bind((proxy_host, proxy_port))
    server.listen(5)

    print(f"[*] Listening on {proxy_host}:{proxy_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
    
    
    


