import socket
import sys
from bs4 import BeautifulSoup
import ssl
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import requests
import time

session=requests.Session()

#function(fetch_obj) will take host,port and url as parameters for fetching the object from the server
def fetch_obj(host, port, url):
    #This socket will be used for establishing a connection to the remote server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #It is used to connect with the server with port and host address
    client_socket.connect((host, port))
    #443 is the port number of the HTTPS
    if(port == 443):
        #it creates an SSL context
        context = ssl.create_default_context()
        #Wrapping the socket for secure communication when connecting to an HTTPS server.
        client_socket = context.wrap_socket(client_socket, server_hostname=host)
        
    
    session = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    print(f"Sending HTTP parallel request to {host}:{port}")
    #Client will send the request to the server by encoding the message
    client_socket.send(session.encode())
    
    parsed_url = urllib.parse.urlparse(url)
    
    #initialized as an empty bytes object
    byteResponse = b""
    #setting the timeout with 10 seconds for recieving the data from the server
    client_socket.settimeout(10)
    
    try:
        while True:
            #recieving the response with 4096 Bytes
            response_chunk = client_socket.recv(4096)
            if not response_chunk:
                break
            # It appends each received Response to the byteResponse variable.
            byteResponse += response_chunk
    except:
        pass
    
    # Process the HTTP response by splitting the responses
    response_parts = byteResponse.split(b'\r\n\r\n', 1)
    
    if len(response_parts) == 2:
        #It is used to store the response data and headers in the separate variables 
        headers, obj_data = response_parts
        # decode the Header and store the status and remaining part in separate variables
        status_line, *header_lines = headers.decode('utf-8').split('\r\n')
        #storing the status code in the new variable (ex:200)
        status_code = status_line.split()[1].encode('utf-8')
        
        if status_code == b'200':
            obj_name = os.path.basename( parsed_url.path)
            obj_path = os.path.join('objects', obj_name)
            
            
            # Save the image to a file
            with open(obj_path, 'wb') as obj_file:
                #saving the object into the file
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
     #It is used to connect with the server with port and host address
    client_socket.connect((host, port))
    
     #443 is the port number of the HTTPS
    if(port == 443):
        #it creates an SSL context
        context = ssl.create_default_context()
        #Wrapping the socket for secure communication when connecting to an HTTPS server.
        client_socket = context.wrap_socket(client_socket, server_hostname=host)
        
    session = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    # Send the request to the server or proxy
    print(f"Sending HTTP request to {host}:{port}")
    #Client will send the request to the server by encoding the message
    client_socket.send(session.encode())

    # Receive and print the response
    byteResponse = b""
     #setting the timeout with 10 seconds for recieving the data from the server
    client_socket.settimeout(5)
    
    try:
        while True:
            #recieving the response with 4096 Bytes
            response_chunk = client_socket.recv(4096)
            # print("inside loop")
            if not response_chunk:
                break
            # It appends each received Response to the byteResponse variable.
            byteResponse += response_chunk
    except:
        pass
    #Closing the socket 
    client_socket.close()
    #Decoding the byteresponse and storing in response_text variable
    response_text = byteResponse.decode()

   #creates a BeautifulSoup object  from the response_text using the 'html.parser' parser
    soup = BeautifulSoup(response_text, 'html.parser')
    # getting the text from the HTML document and storing in the text variable
    text = soup.get_text
    print(f"text : {text}")
    # list will be used to store the URLs of objects found in the HTML content
    object_tags=[]
    # handle image
    img_tags =soup.find_all("img")
    print("Number of img_tags : "+ str(len(img_tags)))
    if len(img_tags)!=0:
         for img in img_tags:
            #extracts the 'src' attribute from the image tags
            img_src = img['src']
             #it is used to append those attributes to the object_tags
            object_tags.append(img_src)
            
    else:
        print("No img tags found on the web page.")
        print()
           
    #This line uses BeautifulSoup to find all <a> (anchor) tags and stores in the link_tags
    link_tags = soup.find_all("a")
    print("Number of link_tags : "+ str(len(link_tags)))
    #creates a BeautifulSoup object  from the response_text using the 'html.parser' parser
    soup = BeautifulSoup(response_text, 'html.parser')
    #It  retrives the text from the soup
    text = soup.get_text
    #printing the text which is extracted 
    print(f"text : {text}")
   
    
    object_tags=[]
    # handle image
    img_tags =soup.find_all("img")
    print("Number of img_tags : "+ str(len(img_tags)))
    if len(img_tags)!=0:
         for img in img_tags:
            img_src = img['src']
            object_tags.append(img_src)
            
    else:
        print("No img tags found on the web page.")
        print()
           
    # handle link
    link_tags = soup.find_all("a")
    print("Number of link_tags : "+ str(len(link_tags))) 
    ##creates a BeautifulSoup object  from the response_text using the 'html.parser' parser
    soup = BeautifulSoup(response_text, 'html.parser')
    text = soup.get_text
    print(f"text : {text}")
  
    # list will be used to store the URLs of objects found in the HTML content
    object_tags=[]
    # handle image
    img_tags =soup.find_all("img")
    print("Number of img_tags : "+ str(len(img_tags)))
    if len(img_tags)!=0:
         for img in img_tags:
            img_src = img['src']
            object_tags.append(img_src)
            
    else:
        print("No img tags found on the web page.")
        print()
           
    # handle link
    link_tags = soup.find_all("a")
    print("Number of link_tags : "+ str(len(link_tags)))

    # handle script
    script_tags = soup.find_all("script")
    print("Number of script_tags: "+ str(len(script_tags)))
    if len(script_tags) != 0:
        for script in script_tags:
            if 'src' in script.attrs:
                script_src = script['src']
                object_tags.append(script_src)
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
            # Get the source (src) attribute of the img tag
            icon_src = icon.get('href')
            object_tags.append(icon_src)
    else:
        print("No icon tags found on the web page.")
        print()
        
    
    print(f"Total number of obj: {len( object_tags)}")
    
    max_threads = len( object_tags)
    with ThreadPoolExecutor(max_threads) as executor:
        for obj in object_tags:
            executor.submit(fetch_obj, host, port, obj)

        
    print("Parsing is Completed")

def main():
    if len(sys.argv) < 4:
        print("Give arguments as: python3 speedyClient.py <host> <port> <path> ")
        sys.exit(1)

    # print(f"Length od arguments: {len(sys.argv)}")
    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    
    t1=time.time()
    send_http_request(host, port, path)
    t2=time.time()
    total_time = t2-t1
    print("Total e2e time = ", total_time )

if __name__ == "__main__":
    main()
