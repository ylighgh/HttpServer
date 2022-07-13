# https_server

An https server built with socket and ssl in python and a client imitating curl behavior, supporting custom request headers and using proxy server functions

## Environmental requirements
```
Python3+
```

## Usage
```
git clone https://github.com/ylighgh/https_server.git
```

### Start the server
```
cd https_server 

python3 https_server.py
```

### Client access
```
./purl.py -U https://xxx.com/
```

## Other
```
╰─ ./purl.py -h                          
usage: purl.py [-h] [--data DATA] [--method METHOD] [--header HEADER] [--url URL] [--proxy PROXY]

Purl

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -D DATA  POST'data
  --method METHOD, -X METHOD
                        requested action(GET,POST,DELETE)
  --header HEADER, -H HEADER
                        custom request headers such as:application/json
  --url URL, -U URL    The address to be accessed, the necessary parameters
  --proxy PROXY, -P PROXY
                        Set the proxy address only supports Http proxy For example:http://127.0.0.1:1080
```
