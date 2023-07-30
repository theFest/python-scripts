"""
Python script is designed to automate the deployment process to multiple remote hosts listed in a CSV file named hosts.csv. It utilizes the paramiko library, which provides SSH functionality, to securely establish connections to each remote host and execute the specified deployment command.
"""

import csv
import paramiko
import getpass
import os

def deploy_to_host(host, username, password, ssh_key=None, deployment_command=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if ssh_key:
            ssh.connect(host, username=username, key_filename=ssh_key)
        else:
            ssh.connect(host, username=username, password=password)

        print(f"Successfully connected to {host}")

        if deployment_command:
            stdin, stdout, stderr = ssh.exec_command(deployment_command)
            print(f"Deployment command output for {host}:")
            print(stdout.read().decode())
        else:
            print("No deployment command provided. Please specify a deployment command.")

    except paramiko.ssh_exception.AuthenticationException as e:
        print(f"Authentication failed for {host}: {e}")
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH error occurred for {host}: {e}")
    except paramiko.BadHostKeyException as e:
        print(f"Bad host key for {host}: {e}")
    except Exception as e:
        print(f"Error connecting to {host}: {e}")
    finally:
        ssh.close()

# Read the CSV file
try:
    with open('hosts.csv', 'r') as f:
        reader = csv.reader(f)
        # Skip the header row
        next(reader)

        for row in reader:
            host, username, password, ssh_key, deployment_command = row

            if not (host and username and (password or ssh_key)):
                print(f"Invalid entry for host: {host}. Skipping.")
                continue

            if ssh_key and not os.path.isfile(ssh_key):
                print(f"SSH key file not found: {ssh_key}. Skipping.")
                continue

            deploy_to_host(host, username, password, ssh_key, deployment_command)

except FileNotFoundError as e:
    print(f"Error opening file: {e}")
except Exception as e:
    print(f"Error reading file: {e}")
