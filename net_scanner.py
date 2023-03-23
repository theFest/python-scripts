""" This is a simple Python script that performs a basic network scan. The script takes in an IP address from the user and then performs a port scan on the given IP address range. The script uses the socket library in Python to establish a connection with the IP address and port 135. If the connection is successful, the script outputs that the IP address is "live." The script also calculates the total time it took to perform the scan and outputs it at the end.
The script starts by importing the socket library and the datetime library. Then, the user is prompted to enter the IP address. The IP address is then split into its individual octets and concatenated to form the base address that the scan will be performed on. The user is also prompted to enter the starting and ending numbers for the IP address range. The script sets the default timeout to 1 second.
The script has two functions: scan() and run1(). The scan function takes an IP address as input and creates a socket connection to the IP address on port 135. If the connection is successful, the function returns a 1, and if not, it returns a 0. The run1() function uses a for loop to iterate through the IP address range and performs a scan on each IP address by calling the scan function. If the scan function returns a 1, the IP address is considered "live" and is printed out. After all the scans have been performed, the script outputs the total time it took to perform the scan. """

import socket
from datetime import datetime
net = input("Enter the IP address: ")
net1 = net.split('.')
a = '.'

net2 = net1[0] + a + net1[1] + a + net1[2] + a
st1 = int(input("Enter the Starting Number: "))
en1 = int(input("Enter the Last Number: "))
en1 = en1 + 1
t1 = datetime.now()

def scan(addr):
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   socket.setdefaulttimeout(1)
   result = s.connect_ex((addr,135))
   if result == 0:
      return 1
   else :
      return 0

def run1():
   for ip in range(st1,en1):
      addr = net2 + str(ip)
      if (scan(addr)):
         print (addr , "is live")

run1()
t2 = datetime.now()
total = t2 - t1
print ("Scanning completed in: " , total)
