import socket # imports the Python socket module
import sys # imports the sys module
from bs4 import BeautifulSoup #imports the BeautifulSoup class 
import ssl # it provides tools for working with SSL/TLS encryption
import os # imports the os module, which provides a way to interact with the operating system
import urllib.parse #imports the urllib.parse module, which contains functions for parsing and manipulating URLs
from concurrent.futures import ThreadPoolExecutor # imports the ThreadPoolExecutor class from the concurrent.futures module
import time #imports the time module, which provides functions for measuring time and adding delays in code


#fetch_obj is a function which takes host,part no,url of the website
def fetch_obj(host, port, url):
    #creating the socket whick is of type tcp(connection oriented)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
     #443 is the port number of the HTTPS it creates an SSL context
    #Wrapping the socket for secure communication when connecting to an HTTPS server.
    if(port == 443):
        context = ssl.create_default_context()
        client_socket = context.wrap_socket(client_socket, server_hostname=host)
        
    
    request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    #Client will send the request to the server by encoding the message
    print(f"Sending GET request for object {url}")
    client_socket.send(request.encode())
    parsed_url = urllib.parse.urlparse(url)
    
    # Receive and print the response
    byteResponse = b""
     #setting the timeout with 10 seconds for recieving the data from the server
    client_socket.settimeout(1)
    
    #recieving the response with 4096 Bytes
    try:
        while True:
            response_chunk = client_socket.recv(4096)
            if not response_chunk:
                break
            byteResponse += response_chunk
    except:
        pass
    
    # Process the HTTP response by splitting the responses
    response_parts = byteResponse.split(b'\r\n\r\n', 1)
    
    if len(response_parts) == 2:
        #It is used to store the response data and headers in the separate variables 
        headers, obj_data = response_parts
        status_line, *header_lines = headers.decode('utf-8').split('\r\n')
        status_code = status_line.split()[1].encode('utf-8')
        
        if status_code == b'200':
            obj_name = os.path.basename( parsed_url.path)
            obj_path = os.path.join('objects', obj_name)
            
            with open(obj_path, 'wb') as obj_file:
                obj_file.write(obj_data)
             #printing the saved data
            print(f"obj saved: {obj_name}")
            print()
            
        else:
            print(f"Failed to download obj: {obj_name}")
            print()
    else:
        print("Invalid HTTP response")
        
    #closing the socket connection
    client_socket.close()
    
#Function which is used to send the http request
def send_http_request(host, port, path):
    
    print(f"Connecting directly to the web server at {host}:{port}")
    #This socket will be used for establishing a connection to the remote server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    #443 is the port number of the HTTPS
    if(port == 443):
        context = ssl.create_default_context()
        client_socket = context.wrap_socket(client_socket, server_hostname=host)
        
    session = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    # Send the request to the server or proxy
    print(f"Sending HTTP request to {host}:{port}")
    client_socket.send(session.encode())

    # Receive and print the response
    byteResponse = b""
    #setting the timeout with 5 seconds for recieving the data from the server
    client_socket.settimeout(5)
    
    try:
        while True:
            response_chunk = client_socket.recv(4096)
            if not response_chunk:
                break
            byteResponse += response_chunk
    except:
        pass
    
    #Closing the socket
    client_socket.close()
    response_text = byteResponse.decode()
    
    extention =""
    if(path != "/"):
            extention = path.split(".")[-1]
            if(extention!= ""):
                print(f"File type is: {extention}")
                name= path.split(".")[0]
                name = name.split("/")[-1] 
                filename = name + "." + extention
                with open(filename, "w", encoding="utf-8") as file:
                        file.write(response_text)
                        print(f"File saved as: {filename}")
            else:
                pass
    if(path == "/" or extention == "html" or extention == "HTML"):
        basehtml = BeautifulSoup(response_text, 'html.parser')
        title = basehtml.title
        print(f"title : {title}")
        object_tags=[]
        
        # handle image
        img_tags =basehtml.find_all("img")
        print("Number of img_tags : "+ str(len(img_tags)))
        if len(img_tags)!=0:
            for img in img_tags:
                #extracts the 'src' attribute from the image tags
                img_src = img['src']
                object_tags.append(img_src)
                
        else:
            print("No img tags found on the web page.")
            print()
            
        # #This line uses BeautifulSoup to find all <a> (anchor) tags and stores in the link_tags
        link_tags = basehtml.find_all("a")
        print("Number of link_tags : "+ str(len(link_tags)))

        # searches for all <script> tags in the HTML content parsed by BeautifulSoup and stores them in the script_tags variable
        script_tags = basehtml.find_all("script")
        print("Number of script_tags: "+ str(len(script_tags)))
        if len(script_tags) != 0:
            for script in script_tags:
                if 'src' in script.attrs:
                    #if <script> tag has a 'src' attribute then it will be stored in script_src variable
                    script_src = script['src']
                    object_tags.append(script_src)
                else:
                    pass
            
        else:
            print("No script tags found on the web page.")
            print()
        
    
    #  searches for <link> elements with the attribute rel set to either "shortcut icon" or "icon" in the HTML content parsed by BeautifulSoup
        icon_tags =basehtml.find_all("link", rel="shortcut icon") or basehtml.find_all("link", rel="icon")
        print("Number of icon_tags : "+ str(len(icon_tags)))
        if len(icon_tags)!=0:
            for icon in icon_tags:
                # etrieves the value of the 'href' attribute for the current <link
                icon_src = icon.get('href')
                object_tags.append(icon_src)
        else:
            print("No icon tags found on the web page.")
            print()
            
        
        print(f"Total number of obj: {len( object_tags)}")
        #calculates the maximum number of threads
        max_threads = len( object_tags)
        with ThreadPoolExecutor() as executor:
            for obj in object_tags:
                executor.submit(fetch_obj, host, port, obj)
            
        print("Parsing is Completed")

def main():
    if len(sys.argv) < 4:
        print("Give arguments as: python3 speedyClient.py <host> <port> <path> ")
        sys.exit(1)

   
    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    
    t1=time.time()
    send_http_request(host, port, path)
    t2=time.time()
    #calculating the total time
    total_time = t2-t1
    print("Total e2e time = ", total_time )

if __name__ == "__main__":
    main()
