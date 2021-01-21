import socket
import sys

addresses = []

def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')


def main():
    sock = socket.socket(socket.AF_INET, 
                         socket.SOCK_DGRAM) 
    port = int(sys.argv[1])       
    print(port, "numarali port dinlemeye gecildi")              
    sock.bind(("", port))
    while True:
        data, addr = sock.recvfrom(1024) 
        print(addr, " ip numarali peer baglandi")
        addresses.append(addr)
        if len(addresses) >= 2:
            print(addresses[0], " numarali ip'ye peer'inin ip'si ve portu gonderildi")
            sock.sendto(addr_to_msg(addresses[1]), addresses[0])
            print(addresses[1], " numarali ip'ye peer'inin ip'si ve portu gonderildi")
            sock.sendto(addr_to_msg(addresses[0]), addresses[1])
            addresses.pop(1)
            addresses.pop(0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("dosyaAdi.py dinlenecekPort seklinde calistirmalisiniz")
        exit(0)
    else:
        main()