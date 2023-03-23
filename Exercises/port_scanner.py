# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 23:41:52 2023

@author: fwhite
"""

import socket
from datetime import datetime


def is_host_up(ip):
    """
    Check if a given IP address is up by pinging it
    :param ip: IP address as string
    :return: True if host is up, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as s:
            s.settimeout(1)
            s.connect((ip, 80))
            return True
    except:
        return False


def scan(ip, port):
    """
    Check if a given IP address and port are open
    :param ip: IP address as string
    :param port: port number as integer
    :return: True if port is open, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            return result == 0
    except:
        return False


def scan_range(ip, start_port, end_port):
    """
    Scan a range of ports on a given IP address
    :param ip: IP address as string
    :param start_port: starting port number as integer
    :param end_port: ending port number as integer
    :return: list of open ports as integers
    """
    open_ports = []
    for port in range(start_port, end_port+1):
        if scan(ip, port):
            open_ports.append(port)
    return open_ports


if __name__ == '__main__':
    ip_address = input("Enter the IP address to scan: ")

    if not is_host_up(ip_address):
        print("Host is not up")
        exit()

    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))

    if start_port > end_port:
        print("Starting port number should be less than or equal to ending port number")
        exit()

    ip_parts = ip_address.split('.')
    if len(ip_parts) != 4:
        print("Invalid IP address")
        exit()

    for part in ip_parts:
        if not part.isdigit() or int(part) < 0 or int(part) > 255:
            print("Invalid IP address")
            exit()

    t1 = datetime.now()
    open_ports = scan_range(ip_address, start_port, end_port)
    t2 = datetime.now()
    total = t2 - t1

    if open_ports:
        print(f"{len(open_ports)} open ports found:", open_ports)
    else:
        print("No open ports found")

    print(f"Scanning completed in {total.total_seconds()} seconds")
