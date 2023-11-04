import socket
import sys
from bs4 import BeautifulSoup
import ssl
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import requests
import time


#fetch_obj is a function which takes host,part no,url of the website
def fetch_obj(host, port, url):
    #creating the socket whick is of type tcp(connection oriented)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # establishes a connection to the server specified by the host and port
    client_socket.connect((host, port))
     #443 is the port number of the HTTPS
    if(port == 443):
         #it creates an SSL context
        context = ssl.create_default_context()
        #Wrapping the socket for secure communication when connecting to an HTTPS server.
        client_socket = context.wrap_socket(client_socket, server_hostname=host)
        
    
    request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    print(f"Sending HTTP parallel request to {host}:{port}")
     #Client will send the request to the server by encoding the message
    client_socket.send(request.encode())
    # parses the url,It breaks down the URL into its components
    parsed_url = urllib.parse.urlparse(url)
    
    # Receive and print the response
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
    client_socket.send(session.encode())

    # Receive and print the response
    byteResponse = b""
    #setting the timeout with 5 seconds for recieving the data from the server
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
    #basehtml is used for storing  parsing HTML and XML documents
    basehtml = BeautifulSoup(response_text, 'html.parser')
    #extracts the title tag from the basehtml and it is stored in title
    title = basehtml.title
    print(f"title : {title}")
    # list will be used to store the URLs of objects found in the HTML content
    object_tags=[]
    # handle image
    img_tags =basehtml.find_all("img")
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
                # script_src values are used to append to object_tags
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
             #the 'href' attribute exists in the current <link> element, this line appends the value of icon_src
            object_tags.append(icon_src)
    else:
        print("No icon tags found on the web page.")
        print()
        
    
    print(f"Total number of obj: {len( object_tags)}")
    #calculates the maximum number of threads
    max_threads = len( object_tags)
    with ThreadPoolExecutor(max_threads) as executor:
        for obj in object_tags:
            #submits a task for the fetch_obj function to be executed concurrently in a separate thread and  passes the host, port, and the current obj
            executor.submit(fetch_obj, host, port, obj)
        
    print("Parsing is Completed")

def main():
    if len(sys.argv) < 4:
        print("Give arguments as: python3 speedyClient.py <host> <port> <path> ")
        sys.exit(1)

    # assigns the value of the first command-line argument to the variable host
    host = sys.argv[1]
    #assigns the value of the second command-line argument to the variable port and convert it into the integer form
    port = int(sys.argv[2])
    path = sys.argv[3]
    #records the current time in seconds
    t1=time.time()
    #function is responsible for sending an HTTP request to the specified host and port, requesting the resource at the given path
    send_http_request(host, port, path)
    #This is the ending time
    t2=time.time()
    #calculating the total time
    total_time = t2-t1
    print("Total e2e time = ", total_time )

if __name__ == "__main__":
    main()
