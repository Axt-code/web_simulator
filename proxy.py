import socket
import threading
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl

# Define the proxy's listening address and port
proxy_host = '0.0.0.0'  # Listen on all available interfaces
proxy_port = 8080

def handle_client(client_socket):
    request = client_socket.recv(4096).decode('utf-8')

    # print("Request: "+ request)
    # Parse the request to extract the host and port
   # Parse the request to extract the host and port
    request_lines = request.split('\n')
    print(f"Request : {request:}")
    print()
    print(f"request_line 0: {request_lines[0]}")
    print(f"request_line 1: {request_lines[1]}")
    print(f"request_line 2: {request_lines[2]}")
    first_line = request_lines[0].strip()
    parts = first_line.split(' ')
    # method = parts[0]
    url = parts[1]
    print(f"url: {url}")
    parsed_url = urlparse(url)
    print(f"parsed_url: {parsed_url}")
    third_line = request_lines[2].strip()
    parts2 = third_line.split(' ')
    host = parts2[1].split(":")[0]
    port = int(parts2[1].split(":")[1])
    print(f"host: {host}, port: {port}")


    if not host:
        print("Error: Invalid URL")
        return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    if(port == 443):
            context = ssl.create_default_context()
            server_socket = context.wrap_socket(server_socket, server_hostname=host)
            
    server_socket.connect((host, port))
    
    request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    # Send the request to the server or proxy
    server_socket.send(request.encode())
    
    print("Request send")

    byteResponse = b""
    
    server_socket.settimeout(4)
    
    try:
        while True:
            response_chunk = server_socket.recv(4096)
            # print("inside loop")
            if not response_chunk:
                break
            byteResponse += response_chunk
    except:
        pass
    
    # print("outside loop")
    
    server_socket.close()
    
    
     # Process the HTTP response
    response_parts = byteResponse.split(b'\r\n\r\n', 1)
    
    status_code=""
    
    if len(response_parts) == 2:
        headers, script_data = response_parts
        status_line, *header_lines = headers.decode('utf-8').split('\r\n')
        status_code = status_line.split()[1].encode('utf-8')
        if status_code != b'200':
            error_message = f"Error: Received status code {status_code}"
            print(error_message)
            # You can send an error response to the client here if needed
            client_socket.send(error_message.encode())
        
    print(f"status code: {status_code.decode('utf-8')}")
    # print(f"header_line: {header_lines}")

    # Modify the response as needed
    # modified_response = response.replace(b'example.com', b'your-proxy-host.com')

    # Send the modified response to the client
    client_socket.send(byteResponse)
        
    

    # Close both sockets
    client_socket.close()


def main():
    # Create a listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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