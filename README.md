# SilentSignal

SilentSignal is a Python-based tool that enables covert communication between a client and a server using ICMP packets. It allows you to send commands from the server to the client and receive the output of the executed commands back at the server, all while maintaining a low profile by using ICMP packets as the communication channel. This tool works when the client is behind NAT.

## Features

- Covert communication using ICMP packets
- Send commands from the server to the client
- Execute commands on the client and receive the output at the server
- Keep-alive functionality to maintain the connection
- Customizable keyword for filtering noise from the internet
- Debugging mode for detailed information during execution

## Prerequisites

- Python 3.x
- Scapy library

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/yourusername/silentsignal.git
```

2. Install the required dependencies:
```
pip install scapy
```
## Usage

 1. Configure the server:
   * Open `server.py` in a text editor.
   * Set the debug variable to 1 for debugging mode or 0 for normal mode.
   * Customize the keyword for filtering noise by modifying the `if result == "your_custom_keyword":` line.


2. Configure the client:
   * Open `client.py` in a text editor.
   * Set the `server_ip` variable to the IP address of your server.
   * Customize the keyword for filtering noise by modifying the `if cmd == "your_custom_keyword":` line.
3. Start the server: (root or sudo probably required here)
   * Run the following command on the cloud server:
     ```
     python3 server.py
     ```
4. Start the client:
   * Run the following command: (sudo/admin is more than likely required here)
     ```
     sudo python3 client.py
     ```
5. Send commands from the server:
   * On the server side, you will be prompted to enter commands to send to the client.
   * Type the command and press Enter to send it to the client.
   * The client will execute the command and send the output back to the server.
6. Exit the tool:
   * To exit the tool, type exit as the command on the server side.

## Customization
  * Customize the keep-alive interval:
    * In `client.py`, modify the `time.sleep(1)` line to set the desired interval between keep-alive pings.
  * Change the custom keyword:
    * In both `server.py` and `client.py`, modify the:
      ```if result == "your_custom_keyword":```
      and
      ```if cmd == "your_custom_keyword":```
      lines to use a unique and hard-to-guess keyword for filtering noise from the internet.
  * I'm not sure if this is required, but I had already done it because I was testing tools built by other people prior to creating my own:
    * add `net.ipv4.icmp_echo_ignore_all=1` to `/etc/sysctl.conf` on both machines? (maybe just the cloud server?) - then run `sysctl -p`
## Disclaimer
This tool is intended for educational and legitimate purposes only. Misuse of this tool may violate laws and regulations. The authors and contributors are not responsible for any misuse or damage caused by this tool.
## License
This project is licensed under the MIT License.
     
