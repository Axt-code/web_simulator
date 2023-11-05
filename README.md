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
 

## Server

   Simple web server: This Python script is a basic HTTP server that listens for incoming client connections, processes HTTP requests, and serves files from the local file system. It handles multiple client connections concurrently using multithreading.  In our case, we have a hello.html file, whenever a client requests for this file, it is served by the server. The client parses this hello.html and displays the output. Our web browser is hosted on port 6789. If the file cannot be located, it will trigger a 404 error. And print requested objects not found.for Simple web server and client
        
   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/7482d626-3ac4-4a14-8097-65464b2fcdd6)

     
       python3 webserver.py


## Client
   Here in this code we are connecting client to the web server or web proxy .
   client send the get request to the server to get the index file .With the help of the index file we can abstract the         Image ,Script and Icons from the index file.For abstacting these Image ,Script and Icons we are sending the TCP Requests 
   to the server.
   - How to Run?              
     python3 client.py <Server Hostname> <Port> <Path>
     
   ### Case (i) : Client-OurWebServer
   
   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/d9e82426-1ba2-4af8-9743-52074a4c2e33)

      python3 Client.py <IP shown at server console> 80 hello.html



   ### Case (ii) : Client-CSEIITH-Page
   
   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/8d8056f1-49a9-40c8-a67c-947209f76d20)

       python3 Client.py cse.iith.ac.in 443 /


   
### Extension: SpeedyClient
   Speedy client uses parallel and persistant TCP connections to get the responses very fast. Speedy client take less time to get the responses when compared to the normal client.

   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/2a9315ca-d920-4484-b054-49deae2d362e)


   ## Case (i) : SpeedyClient-OurWebServer   
      python3 speedyClient.py <IP shown at server console> 80 hello.html

   ## Case (ii) : SpeedyClient-CSEIITH-Page  
      python3 speedyClient.py cse.iith.ac.in 443 /


## Proxy
   This code implements a simple HTTPproxy server.It listens client connection,forwards their HTTP requeststo target servers ,modifies the server's responses by adding proxy host information to the hearders and sends the modified responses back to the clients.The proxy server can handle multiple client connections concurrently,allowing it to intercept and modify traffic passing through it.If proxy accepts the request then it will print status code:200 ok,else it will print 404 error.After getting 200 ok status code the header will be modified.
   
   ## Case (i) : Client-Proxy-OurWebServer   

   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/7482d626-3ac4-4a14-8097-65464b2fcdd6)

       python3 client.py <IP shown at server console> 80 hello.html <Proxy IP> <Proxy port- 6789>

   ## Case (ii) : Client-Proxy-CSEIITH-Page  

   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/cd6e6dcd-e0e9-43df-bcb1-7b7c47e64e3c)

       python3 client.py cse.iith.ac.in 443 / <Proxy IP> <Proxy port- 6789>

   ## How to set proxy in Browser

   Add your proxy in Network settings in the browser


   ![image](https://github.com/Axt-code/ACN-Assigments/assets/40199249/2772357d-7b6c-4e4c-9ed8-4c39740d9dce)

      


   
       
 
