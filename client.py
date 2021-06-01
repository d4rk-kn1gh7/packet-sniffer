#!/usr/bin/env python3

import socket
import pwn
import os
import logging
import argparse
import requests

class NetworkCapture():

    ethproto = {0x0806: 'ARP', 0x0800: 'IPv4', 0x86dd: 'IPv6'}
    netproto = {1: "ICMP", 17: "UDP", 6: "TCP"}

    def __init__(self):
        self.finalData = dict()

    def getTCPdata(self, data):
        proto = pwn.u16(data[12:14], endian = 'big')
        self.finalData['ethproto'] = self.ethproto[proto]
        logging.info(f'Ethernet protocol: {self.ethproto[proto]}')
        data = data[14:]

        #Only ipv4 packets
        if self.ethproto[proto] == 'IPv4':
            proto = pwn.u8(data[9:10])
            src_ip = '.'.join(map(str,data[12:16]))
            dest_ip = '.'.join(map(str,data[16:20]))
            self.finalData['netproto'] = self.netproto[proto]
            self.finalData['src_ip'] = src_ip
            self.finalData['dest_ip'] = dest_ip

            logging.info(f'Protocol: {self.netproto[proto]}, Source IP: {src_ip}, Destination IP: {dest_ip}')
            data = data[20:]

            #Only TCP
            if self.netproto[proto] == 'TCP':
                src_port = pwn.u16(data[:2], endian = 'big')
                dest_port = pwn.u16(data[2:4], endian = 'big')

                self.finalData['src_port'] = src_port
                self.finalData['dest_port'] = dest_port
                logging.info(f'Source Port: {src_port}, Destination Port: {dest_port}')
                data = data[20:]
                
                #If we get an HTTP packet
                if (src_port == 80 or dest_port == 80) and len(data) > 0:
                    logging.info("HTTP!!!")
                    if dest_port == 80:
                        website = self.dns_lookup(dest_ip)
                    else:
                        website = self.dns_lookup(src_ip)
                    logging.info(f"Website: {website}")
                    self.finalData['website'] = website

                #If we get HTTPS
                elif (src_port == 443 or dest_port == 443) and len(data) > 0:
                    logging.info("HTTPS!!!")
                    if dest_port == 443:
                        website = self.dns_lookup(dest_ip)
                    else:
                        website = self.dns_lookup(src_ip)
                    logging.info(f"Website: {website}")
                    self.finalData['website'] = website

        return self.finalData
        
    def dns_lookup(self, ip):
        data = os.popen(f"dig +noall +answer -x {ip}", "r").read()
        return data.split(" ")[-1].split("\t")[-1].replace("\n", "")

class Client():

    def __init__(self, server, device, interface):
        self.server = server
        self.device = device
        self.interface = interface

    def exec(self):
        sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        if self.interface is not None:
            sock.bind((self.interface, 0))
        self.capture(sock)
        
    def capture(self, sock):
        while True:
            data = sock.recv(65565)
            net_cap = NetworkCapture()
            output = net_cap.getTCPdata(data)
            self.send2server(output)
            
    def send2server(self, output):
        url = f"http://{self.server}:9000/capturer"
        output['device_name'] = self.device
        output['confirm'] = "success"
        try:
            r = requests.post(url, output)
            print(r.text)
            if "Data Received!" in r.text:
                logging.info("Sent data!")
            else:
                logging.error("Unable to send data!!!")
        except Exception as e:
            logging.error(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Packer Sniffer - Client")
    parser.add_argument("-s", "--server", help = "Server IP", required = True)
    parser.add_argument("-i", "--interface", help = "Interface", required = False, default = None)
    parser.add_argument("-d", "--device", help = "Device name", required = False, default = os.uname()[1])

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    try:
        c = Client(server = args.server, device = args.device, interface = args.interface)
        c.exec()

    except Exception as e:
        logging.error(e)
