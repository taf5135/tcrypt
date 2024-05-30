from math import ceil
from bitops import rotate_left, rotate_right
from TSymCipher import TSymCipher

#Objective:
#Use only bit-fiddling operations to create a super fast cipher
#&, |, ^, ~, >>, and the Rotate functions will be useful

BIT_MASK_64 = 0xFFFFFFFFFFFFFFFF

#Four registers each 64 bits long
class Twiddler(TSymCipher):

    def __init__(self, state, nonce=0):
        super().__init__(state)

        #Each of these is 64 bits long to make computations easy
        self.reg1 = state >> 192 & BIT_MASK_64
        self.reg2 = state >> 128 & BIT_MASK_64
        self.reg3 = state >> 64  & BIT_MASK_64
        self.reg4 = state        & BIT_MASK_64

        self.cache = []

        for _ in range(64): #Ensures every bit propagates to every other
            self.clock()

        #TODO clock the cipher 32 times (at least, probably more) to set up the state
        #TODO should have some kind of IV perhaps to ensure that 
    
    #Just performs a 64-bit xorshift operation on the input
    #Known to have a long period, but fails many linear recurrence tests
    #Taken directly from sample implementation because the algorithm is so simple
    def xorshift(self, register):
        register ^= register << 13
        register ^= register >> 7
        register ^= register << 17
        return register

    def xorshift_alternate(self, register):
        register ^= register << 7
        register ^= register >> 9
        return register

    #Returns 8 bytes
    def clock(self):
        #75 operations excluding function calls
        reg1 = rotate_left(reg1, 1, 64)
        reg2 = rotate_right(reg2, 1, 64)
        reg3 = rotate_left(reg3, 1, 64)
        reg4 = rotate_right(reg4, 1, 64)
        reg1_next = (self.xorshift(reg2) & self.xorshift_alternate(reg3)) ^ self.xorshift(reg4) ^ self.xorshift(reg1)
        reg2_next = (self.xorshift(reg1) & self.xorshift_alternate(reg2)) ^ self.xorshift(reg3) ^ self.xorshift(reg2)
        reg3_next = (self.xorshift(reg1) & self.xorshift_alternate(reg3)) ^ self.xorshift(reg2) ^ self.xorshift(reg3)
        reg4_next = (self.xorshift(reg2) & self.xorshift_alternate(reg3)) ^ self.xorshift(reg1) ^ self.xorshift(reg4)
        reg1, reg2, reg3, reg4 = reg1_next, reg2_next, reg3_next, reg4_next
        return list((reg1 ^ reg2 ^ reg3 ^ reg4).to_bytes(8, 'big'))


    def getbytes(self, n):

        out_bytes = self.cache[:n]
        n -= len(self.cache)

        rounds = ceil(n / 8)

        round_bytes = []
        for r in range(rounds):
            round_bytes += self.clock()
        self.cache = round_bytes[n:]
        out_bytes += round_bytes[:n] 
        return out_bytes


    def getbyte(self):
        if self.cache == []:
            computed_bytes = self.clock()
            self.cache = computed_bytes[1:]
            return computed_bytes[0]
        else:
            dq = self.cache[0]
            self.cache = self.cache[1:]
            return dq
    """
    Swap bits:

    unsigned int i, j; // positions of bit sequences to swap
    unsigned int n;    // number of consecutive bits in each sequence
    unsigned int b;    // bits to swap reside in b
    unsigned int r;    // bit-swapped result goes here

    unsigned int x = ((b >> i) ^ (b >> j)) & ((1U << n) - 1); // XOR temporary
    r = b ^ ((x << i) | (x << j));
    """

    """
    Reverse one byte: 

    b = ((b * 0x80200802ULL) & 0x0884422110ULL) * 0x0101010101ULL >> 32;

    """