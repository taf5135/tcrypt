#Use this for whatever cryptography stuff you want to make

#designing my own cipher
#write in Python, maybe rewrite in C, test with BigCrush 
import subprocess
import time

from TSymCipher import TSymCipher
from ChangingState import ChangingState


def do_crypt(file_in, file_out, cipher : TSymCipher):   

    batch_size = 5000000
    with open(file_in, 'rb') as fin:
        with open(file_out, 'wb') as fout:
            while (in_bytes := fin.read(batch_size)): 
                blen = len(in_bytes)
                keystream = cipher.getbytes(blen)
                cstream = [in_bytes[i] ^ keystream[i] for i in range(blen)]
                fout.write(bytes(cstream))


def changingstate_basic_test():
    uint = int.from_bytes([ord('U') for _ in range(32)], 'big')
    c = ChangingState(uint, 0)
    #test permutation
    print(f"Initial state: {bin(c.state)}")
    newstate = c._permute(c.state, c.permbox)
    print(f"Permuted state: {bin(newstate)}")
    #test substitution
    newstate = c._substitute(newstate, c.sbox)
    print(f"Substituted state: {hex(newstate)}")

    newstate = c._expand(newstate)
    print(f"Expanded state: {hex(newstate)}")

    c.state = uint
    substate = c._substitute(c.state, c.sbox)
    print(f"Subbed from original state: {bin(substate)}")


def changingstate_full_test():
    uint = int.from_bytes([ord('U') for _ in range(32)], 'big')
    c = ChangingState(uint, 0)
    d = ChangingState(uint, 0)
    cbyte = c.getbyte()
    assert c.cache[0]==c.getbyte()

    #test get_bytes in various conditions (no cache, some cache, generating different amounts of bytes, etc)
    dbyte = d.getbytes(2)[0]
    assert c.state == d.state
    assert cbyte == dbyte
    assert c.cache == d.cache


    #testing get bytes: save the cache, call getbytes(256), see if the cache matches what it output and how much is left.
    dbytes_next = d.getbytes(255)
    assert len(dbytes_next) == 255
    assert len(d.cache) == 31

    dbytes_next = d.getbytes(511)
    assert len(dbytes_next) == 511
    assert len(d.cache) == 1


def megabyte_speedtest():
    uint = int.from_bytes([ord('U') for _ in range(32)], 'big')
    c = ChangingState(uint, 0)
    t1 = time.process_time()
    for i in range(1000000):
        c.getbyte()
    t2 = time.process_time()
    print(f"Producing 1mb the naiive way takes {t2-t1} secs")

    d = ChangingState(uint, 0)
    t1 = time.process_time()
    d.getbytes(1000000)
    t2 = time.process_time()
    print(f"Producing 1mb in the more clever way takes {t2-t1} secs")


#use this for stubbing things out
def main():

    first = "Narodnya_plain.txt"
    encrypted = "Narodnya_cipher.tcr"
    decrypted = "Narodnya_decrypted.txt"

    cipher = ChangingState(0) #Just replace this with your own cipher class

    do_crypt(first, encrypted, cipher)
    print("Finished encryption")

    cipher.reset()

    do_crypt(encrypted, decrypted, cipher)
    print("Finished decryption")

    #FC file1 file2, windows version of diff
    subprocess.run(["FC", first, decrypted])

    return 0

if __name__ == "__main__":
    main()
    #changingstate_basic_test()
    #changingstate_full_test()
    #megabyte_speedtest()