#!/usr/bin/env python3

import socket
import struct
import pwn
    
class Sniffer():
    ethproto = {0x0806: 'ARP', 0x0800: 'IPv4', 0x86dd: 'IPv6'}
    netproto = {1: "ICMP", 17: "UDP", 6: "TCP"}
    
    def __init__(self, interface = None):
        self.interface = interface
        
    def exec(self):
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        if self.interface is not None:
            sock.bind((self.interface, 0))
        while True:
            raw_data = sock.recv(65565)
            self.parse(raw_data)
            
    def parse(self, raw_data):
        proto = pwn.u16(raw_data[12:14], endian = 'big')
        print(f'Ethernet protocol: {self.ethproto[proto]}')
        data = raw_data[14:]

        #Only ipv4 packets
        if self.ethproto[proto] == 'IPv4':
            proto = pwn.u8(data[9:10])
            src_ip = '.'.join(map(str,data[12:16]))
            dest_ip = '.'.join(map(str,data[16:20]))
            print(f'Protocol: {self.netproto[proto]}, Source IP: {src_ip}, Destination IP: {dest_ip}')
            data = data[20:]
            
            #Only TCP
            if self.netproto[proto] == 'TCP':
                src_port = pwn.u16(data[:2], endian = 'big')
                dest_port = pwn.u16(data[2:4], endian = 'big')
                print(f'Source Port: {src_port}, Destination Port: {dest_port}')
                data = data[20:]
                
                #If we get an HTTP packet
                if src_port == 80 or dest_port == 80 and len(data) > 0:
                    print("HTTP!!!")
                    print(data)
                
if __name__ == "__main__":
    packet = Sniffer()
    packet.exec()