import socket # imports the Python socket module
import sys # imports the sys module
from bs4 import BeautifulSoup #imports the BeautifulSoup class from the bs4 module
import ssl # it provides tools for working with SSL/TLS encryption
import os # imports the os module
import urllib.parse #it contains functions for parsing and manipulating URLs
import time #  imports the time module

def obj_get(host, port, obj_src, proxy_host=None, proxy_port=None):
    try:
        # Create a socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # establishes a connection to the server specified by the host and port
        if proxy_host and proxy_port:
            print(f"Connecting to the proxy at {proxy_host}:{proxy_port}")
            client_socket.connect((proxy_host, proxy_port))
        else:
            print(f"Connecting directly to the web server at {host}:{port}")
            client_socket.connect((host, port))
            
        if(port == 443 and proxy_host==None):
            # line creates an SSL context using the ssl module
            context = ssl.create_default_context()
            client_socket = context.wrap_socket(client_socket, server_hostname=host)
            
        # parses the URL provided in obj_src using the urllib.parse.urlparse function
        parsed_url = urllib.parse.urlparse(obj_src)
        path = parsed_url.path if parsed_url.path else '/'
      
        request = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
            
        # Send the HTTP request by encoding the message
        client_socket.send(request.encode())
        
        response = b''
        #setting the timeout with 30 seconds for recieving the data from the server
        client_socket.settimeout(30)
        
        #recieving the response with 4096 Bytes and storing the message in the data variable
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
        
        # Process the HTTP response by splitting the responses
        response_parts = response.split(b'\r\n\r\n', 1)
        obj_name = os.path.basename(parsed_url.path)
        obj_path = os.path.join('objects', obj_name)
                
        
        if len(response_parts) == 2:
            headers, obj_data = response_parts
            #decodes the headers and splits them
            status_line, *header_lines = headers.decode('utf-8').split('\r\n')
            #extracts the status code and encode them
            status_code = status_line.split()[1].encode('utf-8')
            
            if status_code == b'200':
                
                # Save the object to a file
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
    #creating the socket whick is of type tcp(connection oriented)
    if proxy_host:
        print(f"Connecting to the proxy at {proxy_host}:{proxy_port}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((proxy_host, proxy_port))
    else:
        print(f"Connecting directly to the web server at {host}:{port}")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

    #  line creates an SSL context using the ssl module
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
    #setting the timeout with 30 seconds for recieving the data from the server
    client_socket.settimeout(30)
    
    #recieving the response with 4096 Bytes and storing the message in the data variable
    try:
        while True:
            response_chunk = client_socket.recv(4096)
            if not response_chunk:
                break
            byteResponse += response_chunk
    except:
        pass
    
    client_socket.close()
    #decoding the by byteresponse
    response_text = byteResponse.decode()
    #it is used to parse the resonse_text as HTML parser
    basehtml = BeautifulSoup(response_text, 'html.parser')
    title = basehtml.title
    print(f"\nTitle : {title}\n")
   
    
    #  Process the HTTP response by splitting the responses
    response_parts = byteResponse.split(b'\r\n\r\n')
    
    headers =""
    if len(response_parts) == 2:
        #headers will contain the HTTP response headers, and script_data will contain the content of a script 
        headers, script_data = response_parts
        
    if(headers != ""):    
        print("Header : \n" + headers.decode('utf-8')+"\n")
    
    # handling the image
    img_tags =basehtml.find_all("img")
    print("Number of img_tags : "+ str(len(img_tags)))
    if len(img_tags)!=0:
         for img in img_tags:
            # Get the source (src) attribute of the img tag
            img_src = img['src']
            obj_get(host, port, img_src, proxy_host, proxy_port)
            print()
    else:
        print("No img tags found on the web page.")
        print()
           
    # handle link
    link_tags = basehtml.find_all("a")
    print("Number of link_tags : "+ str(len(link_tags)))
    if len(link_tags)!=0:
         for link in link_tags:
             print(f"Found link: {link}")
             print()
   
    # handle script
    script_tags = basehtml.find_all("script")
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
       
   
   # handle icon and shortcut icon
    icon_tags =basehtml.find_all("link", rel="shortcut icon") or basehtml.find_all("link", rel="icon")
    print("Number of icon_tags : "+ str(len(icon_tags)))
    if len(icon_tags)!=0:
         for icon in icon_tags:
             # extracts the value of the 'href' attribute from an HTML <link>
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
       
    #records the current time in seconds
    t1=time.time()
    send_http_request(host, port, path, proxy_host, proxy_port)
    #records the current time  again in seconds 
    t2=time.time()
    #total time 
    total_time = t2-t1
    print("Total End-to-End time = ", total_time )

if __name__ == "__main__":
    main()
