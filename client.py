import socket
import sys
from bs4 import BeautifulSoup
import ssl
import os
import urllib.parse
import time

def obj_get(host, port, obj_src, proxy_host=None, proxy_port=None):
    try:
        # Create a socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if proxy_host and proxy_port:
            print(f"Connecting to the proxy at {proxy_host}:{proxy_port}")
            client_socket.connect((proxy_host, proxy_port))
        else:
            print(f"Connecting directly to the web server at {host}:{port}")
            client_socket.connect((host, port))
            
        if(port == 443 and proxy_host==None):
            context = ssl.create_default_context()
            client_socket = context.wrap_socket(client_socket, server_hostname=host)
            
        # Construct the HTTP GET request for the image
        parsed_url = urllib.parse.urlparse(obj_src)
        path = parsed_url.path if parsed_url.path else '/'
      
        request = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
            
        # Send the HTTP request
        client_socket.send(request.encode())
        
        response = b''
        
        client_socket.settimeout(30)
        
        try:        
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
        except:
            pass
        
        # Close the client socket
        client_socket.close()
        
        # Process the HTTP response
        response_parts = response.split(b'\r\n\r\n', 1)
        
        # print(f"length tof response_path: {len(response_parts)}")
        
        # print(f"Response: {response_parts}")
        
        obj_name = os.path.basename(parsed_url.path)
        obj_path = os.path.join('objects', obj_name)
                
        
        if len(response_parts) == 2:
            headers, obj_data = response_parts
            status_line, *header_lines = headers.decode('utf-8').split('\r\n')
            status_code = status_line.split()[1].encode('utf-8')
            
            if status_code == b'200':
                
                # Save the image to a file
                with open(obj_path , 'wb') as obj_file:
                    obj_file.write(obj_data)
                
                print(f"Object saved: {obj_name}")
                print()
                
            else:
                print(f"Failed to download obj: {obj_name}")
                print()
        else:
            print("Invalid HTTP response")
    except Exception as e:
        print(f"Error: {e}")

def send_http_request(host, port, path, proxy_host=None, proxy_port=None):
    if proxy_host:
        print(f"Connecting to the proxy at {proxy_host}:{proxy_port}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((proxy_host, proxy_port))
    else:
        print(f"Connecting directly to the web server at {host}:{port}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

    if(port == 443 and proxy_host==None):
        context = ssl.create_default_context()
        client_socket = context.wrap_socket(client_socket, server_hostname=host)
        
    
    # Create an HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
        
    # Send the request to the server or proxy
    print(f"Sending HTTP request to {host}:{port}")
    client_socket.send(request.encode())

    # Receive and print the response
    byteResponse = b""
    
    client_socket.settimeout(30)
    
    try:
        while True:
            response_chunk = client_socket.recv(4096)
            if not response_chunk:
                break
            byteResponse += response_chunk
    except:
        pass
    
    client_socket.close()
    
    response_text = byteResponse.decode()
    
    soup = BeautifulSoup(response_text, 'html.parser')
    text = soup.get_text
    # print(f"text : {text}")
   
    
      # Process the HTTP response
    response_parts = byteResponse.split(b'\r\n\r\n')
    
    headers =""
    if len(response_parts) == 2:
        headers, script_data = response_parts
        # print(f"header: {headers}")
        
    print("Header : " + headers.decode('utf-8')+"\n")
    
    # handle image
    img_tags =soup.find_all("img")
    print("Number of img_tags : "+ str(len(img_tags)))
    if len(img_tags)!=0:
         for img in img_tags:
            # Get the source (src) attribute of the img tag
            img_src = img['src']
            # img_name = os.path.basename(img_src)
            obj_get(host, port, img_src, proxy_host, proxy_port)
            print()
    else:
        print("No img tags found on the web page.")
        print()
           
    # handle link
    link_tags = soup.find_all("a")
    print("Number of link_tags : "+ str(len(link_tags)))
    if len(link_tags)!=0:
         for link in link_tags:
             print(f"Found link: {link}")
             print()
   
    # handle script
    script_tags = soup.find_all("script")
    print("Number of script_tags: "+ str(len(script_tags)))
    if len(script_tags) != 0:
        for script in script_tags:
            if 'src' in script.attrs:
                script_src = script['src']
                print(f"External script source: {script_src}")
                # Call the script_get function to handle external script files
                obj_get(host, port, script_src, proxy_host, proxy_port)
                print()
            else:
                pass
        
    else:
        print("No script tags found on the web page.")
        print()
       
   
   # handle icon
    icon_tags =soup.find_all("link", rel="shortcut icon") or soup.find_all("link", rel="icon")
    print("Number of icon_tags : "+ str(len(icon_tags)))
    if len(icon_tags)!=0:
         for icon in icon_tags:
            icon_src = icon.get('href')
            obj_get(host, port, icon_src, proxy_host, proxy_port)
            print()
            
    else:
        print("No icon tags found on the web page.")
        print()
        
    print("Parsing is Completed")

def main():
    
    if len(sys.argv) < 4:
        print("Give arguments as: python web_client.py <host> <port> <path> [<proxy_host> <proxy_port>]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    proxy_host = None
    proxy_port = None
 
    if len(sys.argv) == 6:
        print(f"all args {sys.argv[0]}, {sys.argv[1]}, {sys.argv[2]}, {sys.argv[3]}, {sys.argv[4]}")
        host = sys.argv[1]
        proxy_host = sys.argv[4]
        proxy_port = int(sys.argv[5])
       

    t1=time.time()
    send_http_request(host, port, path, proxy_host, proxy_port)
    t2=time.time()
    total_time = t2-t1
    print("Total e2e time = ", total_time )

if __name__ == "__main__":
    main()
