# ACN-Assigments

## Folder structure

- Client
   - client.py
  -  objects
  - speedyClient.py
- Proxy
   - proxy.py
- README.md
- Server
    - hello.html
    - webserver.py

## Client
   Here in this code we are connecting client to the web server or web proxy .
   client send the get request to the server to get the index file .With the help of the index file we can abstract the         Image ,Script and Icons from the index file.For abstacting these Image ,Script and Icons we are sending the TCP Requests 
   to the server.
                  to run the Client               
   - `python3 client.py cse.iit.ac.in 443 /`

### SpeedyClient
   Speedy client uses parallel and persistant TCP connections to get the responses very fast. Speedy client take less time to get the responses when compared to the normal client.
                  To run the Speedy client we use 
   - `python3 speedyClient.py cse.iith.ac.in 443 / `

## Server

   This Python script is a basic HTTP server that listens for incoming client connections, processes HTTP requests, and serves files from the local file system. It handles multiple client connections concurrently using multithreading.  In our case, we have a hello.html file, whenever a client requests for this file, it is served by the server. The client parses this hello.html and displays the output. Our web browser is hosted on port 6789. If the file cannot be located, it will trigger a 404 error. And print requested objects not found.for Simple web server and client
   - `python3 webserver.py `
   - `python3 client.py 192.168.0.207



## Proxy
   This code implements a simple HTTPproxy server.It listens client connection,forwards their HTTP requeststo target servers ,modifies the server's responses by adding proxy host information to the hearders and sends the modified responses back to the clients.The proxy server can handle multiple client connections concurrently,allowing it to intercept and modify traffic passing through it.If proxy accepts the request then it will print status code:200 ok,else it will print 404 error.After getting 200 ok status code the header will be modified.
                  To run this we use :
   - `python3 proxy.py`
