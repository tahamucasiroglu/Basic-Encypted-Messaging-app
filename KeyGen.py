import Cryptomath
import RabinMiller
import os
import random
import sys
import IO_Ops


def generateKey(keySize):
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...')
    p = RabinMiller.generateLargePrime(keySize)

    print('p PRIME IS', p)

    # String as hex
    hex_string = hex(p)
    print('Prime p as hex:', hex_string)

    print('Keysize: ', keySize)

    print('Generating q prime...')
    q = RabinMiller.generateLargePrime(keySize)

    print('q PRIME IS', q)

    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if Cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = Cryptomath.findModInverse(e, (p - 1) * (q - 1))
    publicKey = (n, e)
    privateKey = (n, d)
    print('Public key:', publicKey)
    print('Private key:', privateKey)
    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):
    
    publicKey, privateKey = generateKey(keySize)
    print()
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % (name))

    fo = open('%s_pubkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()
    print()
    print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing private key to file %s_privkey.txt...' % (name))

    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()
    # If makeRsaKeys.py is run (instead of imported as a module) call
    # the main() function.


# IOops test start
# IO_Ops.textToDeci('TEST tres')

# IOops test end


def readKeyFiles(filename):
    file = open(filename, "r")
    keyLenght, nVal, eORdVal = "", "", ""

    for line in file:
        fields = line.split(",")

        keyLenght = fields[0]
        nVal = fields[1]
        eORdVal = fields[2]

    #print('Key Lenght:', keyLenght, '\nValue N:', nVal, '\nE or D Value:', eORdVal)
    return keyLenght, nVal, eORdVal


def encryptMessage(plainText, pubKey):
    m = IO_Ops.textToDeci(plainText)
    print(m)
    # l, n, e = readKeyFiles('keys_pubkey.txt')
    temp = pubKey.split(",")
    n = temp[0]
    e = temp[1]
    #print('Encrypted Message:', IO_Ops.constant_time_power(int(m), int(e), int(n)))

    return IO_Ops.constant_time_power(int(m), int(e), int(n))


def decryptMessage(cypherText):

    l, n, d = readKeyFiles('keys_privkey.txt')

    print('L=', l, '\nN=', n, '\nD=', d)


    m = IO_Ops.constant_time_power(int(cypherText), int(d), int(n))
    print('m2=', m)
    plainT = IO_Ops.deciToText(str(m))
    print('Decrypted message:', plainT)
    
    return plainT



