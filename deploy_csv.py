# script in Python to securely deploy to hostnames from a CSV file containing the Hostname, Username, and Password

import csv
import paramiko
import getpass

def deploy_to_host(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    # execute your deployment commands here
    ssh.close()

# read the CSV file
with open('hosts.csv', 'r') as f:
    reader = csv.reader(f)
    # skip the header row
    next(reader)
    for row in reader:
        host, username, password = row
        deploy_to_host(host, username, password)
