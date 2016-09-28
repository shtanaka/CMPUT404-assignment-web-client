#!/usr/bin/env python
# coding: utf-8

class utilsm():

    def get_code( data):
        data = data.split("\r")
        line = data[0].split(" ")
        return int(line[1])

    def get_body(data):
        body = data.partition('\r\n\r\n')[2]
        return body
    
    def get_headers(ata):
        return None

    def get_host(data):
        return data[2].split(":")[0]
    
    def get_path(data):
        if len(data) < 4:
            return "/"
        return data[3]

    def get_port(data):
        r = data[2].split(":")
        if len(r) == 1 :
            return "80"
        return r[1]

    def break_args_post(data):
        param = ""
        for i, v in data.iteritems(): 
            param += i + "=" + v + "&"
        param = param[:-1]
        out = "Content-Length: "+ str(len(param)) + "\r\n"
        out += "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
        out += param
        out += "\r\n"
        return out
    
    def break_url(data):
        data = data.split("/", 3)
        host = et_host(data)
        path = et_path(data)
        port = et_port(data)
        return host, path, port