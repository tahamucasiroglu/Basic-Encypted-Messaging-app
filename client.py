import socket
import sys
import time
import KeyGen

def msg_to_addr(data):
    ip, port = data.decode('utf-8').strip().split(':')
    return (ip, int(port))

def recv_msg(sock, pubKey):
    data, addr = sock.recvfrom(8192)
    decoded = data.decode()
    if pubKey != decoded:
        intedMsg = int(decoded)
        decryptedMsg = KeyGen.decryptMessage(intedMsg)
        return decryptedMsg
    else:
        return " connection successful"

def send_msg(sock, addr, pubKey, data):
    encryptedMsg = KeyGen.encryptMessage(data, pubKey)
    stredMsg = str(encryptedMsg)
    sock.sendto(stredMsg.encode(), addr)
    
def ilkBaglanti(sock, host, port): #serverin host ve portu ile cagrilacak.
    sock.sendto(b'0', (host, port))
    data, addr = sock.recvfrom(8192)
    addr = msg_to_addr(data)
    print('serverden gelen peer datasi adrese cevrilerek saklandi')
    #server bağlantısı bitti

    #key oluşturma
    KeyGen.makeKeyFiles('keys', 1024)
    keyLenght, myKeym, myKeye = KeyGen.readKeyFiles('keys_pubkey.txt')
    publicKey = myKeym + "," + myKeye
    sock.sendto(publicKey.encode(), addr)
    #karşıdan pubkey alır
    data, addr = sock.recvfrom(8192)
    sock.sendto(publicKey.encode(), addr) #bağlantıda hata olmasın diye pubkeyi bir kez daha yolladık
    peersKey = data.decode()
    #bilgilendirme mesajları
    print('karsi tarafin public keyi basariyla alindi')   
    print('karsi tarafin public keyi:', end=" ")
    print(peersKey)
    print('bizim public keyimiz:', end=" ")
    print(publicKey)
    
    return addr, peersKey