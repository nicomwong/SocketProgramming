# server_python_udp.py

# UCSB CS 176A Fall 2020 HW #1 Socket Programming
# Nicholas M Wong, PID: 3018439
# Syntax/libraries learned from geeksforgeeks.org, w3schools.com, docs.python.org

import socket
import sys
import subprocess

# Check for valid cmd line input
if ( len(sys.argv) != 2):
    print("Usage: python server_python_udp.py <port>")
    sys.exit()

# Set the port
port = int(sys.argv[1])
if not(0 <= port <= 65535):
    print("Invalid port number")

# Create a IPv4/UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to this machine with the port
s.bind( ('', port) )

# Infinite loop to wait for client connection
while True:
    
    # Set socket to blocking
    s.setblocking(True)
    
    # Wait to receive command from client
    commandFromClient, addr = s.recvfrom(1024)

    # Run the command on the shell from server and store the output
    stdout = subprocess.check_output( commandFromClient.decode(), shell=True )

    # Put the output into a file
    # f = open("server_udp_stdout.txt", "w")
    # f.write( stdout.decode() )
    # f.close()

    timesSent = 0   # Track the number of times the message has been sent
    while timesSent < 3:

        # Send the message length to the client
        s.sendto(str( len(stdout) ).encode(), addr)

        # Send the command output to the client
        s.sendto(stdout, addr)

        # Set timeout to 1 second
        s.settimeout(1)
        
        # Wait for ACK to be received
        try:
            ack, addr = s.recvfrom(1024)

        # If it takes more than 1 second, resend message and length
        except socket.timeout:
            # Increment times sent
            timesSent += 1

        # Else, check that the data was ACK
        else:
            # If it was not ACK, resend message and length
            if not(ack.decode() == "ACK"):
                # Increment times sent
                timesSent += 1

            # If it was ACK, print ACK received and go idle
            else:
                print("ACK received")
                break
    
    # If timesSent reached 3, print error and ditch this return message
    if timesSent >= 3:
        print("Failed to send command output back to client. Message is ditched")
        continue