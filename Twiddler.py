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

        #TODO clock the cipher 32 times (at least, probably more) to set up the state
        #TODO should have some kind of IV perhaps to ensure that 

    #Returns some number of bytes
    def clock():
        #Steps:
        #1: rotate reg1 and reg3 right, rotate reg2 and reg4 left
        #2: reg1_next = reg2, reg3, reg4 TODO
        #3: reg2_next = reg1, reg3, reg4
        #4: reg3_next = reg1, reg2, reg4
        #5: reg4_next = reg1, reg2, reg3
        #output = 
         
        pass

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