#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
import json

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    
    def __str__(self):
        return self.body

class HTTPClient(object):
    #def get_host_port(self,url):
    
    def connect(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            return sock
        except socket.error:
            return None

    def get_code(self, data):
        data = data.split("\r")
        line = data[0].split(" ")
        return int(line[1])

    def get_body(self, data):
        body = data.partition('\r\n\r\n')[2]
        return body
    
    def get_headers(self,data):
        return None

    def get_host(self, data):
        return data[2].split(":")[0]
    
    def get_path(self, data):
        if len(data) < 4:
            return "/"
        return data[3]

    def get_port(self, data):
        r = data[2].split(":")
        if len(r) == 1 :
            return "80"
        return r[1]

    def break_args(self, data):
        param = ""
        for i, v in data.iteritems(): 
            param += i + "=" + v + "&"
        param = param[:-1]
        out = "Content-Length: "+ str(len(param)) + "\r\n"
        out += "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
        out += param
        out += "\r\n"
        return out

    def break_url(self, data):
        data = data.split("/", 3)
        host = self.get_host(data)
        path = self.get_path(data)
        port = self.get_port(data)
        return host, path, port


    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host, path, port = self.break_url(url)
        request = "GET /" + path + " HTTP/1.1\n"
        request += "User-Agent: MyClient\r\n"
        request += "Host: " + host + "\r\n"
        request += "Accept: */*\r\n\r\n"
        sock = self.connect(host, int(port))
        sock.sendall(request)
        body = self.recvall(sock)
        code = self.get_code(body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, path, port = self.break_url(url)
        request = "POST /" + path + " HTTP/1.1\n"
        request += "User-Agent: MyClient\r\n"
        request += "Host: " + host + "\r\n"
        request += "Accept: */*\r\n"
        if args is not None:
            request += self.break_args(args)
        else:
            request += "\r\n"
        print request
        sock = self.connect(host, int(port))
        sock.sendall(request)
        response = self.recvall(sock)
        body = self.get_body(response)
        code = self.get_code(response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    elif (len(sys.argv) == 2):
        print client.command( sys.argv[1] )
    else:
        print client.command( sys.argv[2], sys.argv[1], sys.argv[3] )   
