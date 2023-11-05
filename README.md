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
   -`python3 client.py cse.iit.ac.in 443 /`

### SpeedyClient
   Speedy client uses parallel and persistant TCP connections to get the responses very fast. Speedy client take less time to get the responses when compared to the normal client.
   To run the Speedy client we use 
   - `python3 speedyClient.py cse.iith.ac.in 443 / `

## Server

## Proxy
