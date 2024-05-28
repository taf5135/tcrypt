from TSymCipher import TSymCipher

from math import ceil

#Ultimately this kind of stream cipher is just a block cipher in a different mode
#But it's fun to write and design
class ChangingState(TSymCipher):

    def __init__(self, state, nonce=0):
        super().__init__(state)

        for i in range(8):
            state ^= (nonce << 64 * i) #TODO test if this works
        self.nonce = nonce
        self.state = state

        
        self.permbox = self.load_box("permbox.txt")
        self.sbox = self.load_box("sbox_ninv.txt") 
        self.out_permbox = self.load_box("out_permbox.txt") 
        self.out_sbox = self.load_box("out_sbox_ninv.txt") 
        self.cache = []

        """
        Description:

        Stream cipher that generates 256 bits of stream per cycle. It takes as input:
        -A 256-bit key
        -a 64-bit nonce

        Per cycle, it outputs:
        -256 bits of keystream (32 bytes)

        It can run for:
        -2^64 cycles (TODO implementation-specific detail)

        Basic Function:
            Initialization:
            -Accept the key and nonce
            -Combine the key with the nonce as follows:
                -split the key into 64 bit blocks
                -XOR the nonce with each block 
                    -With this XOR method, for two nonces that differ by one bit: 
                        -after 1 cycle, 8 bits are different
                        -after 2 cycles, 64 bits are different
                        -after 3 cycles, every byte will be different 
                

            Per Cycle:
            -Feed state into state substitution-permutation network:
                -Permute the state, shifting the bits around according to the permutation box
                -Substitute each byte in the state for a new byte using the substitution box
                    -To prevent known-plaintext attacks, the substitution step must be nonlinear. 
                    -Since the substitution box only outputs values in the range 0-127, we have to expand them. This is done by taking the parity of the byte and the 
                    byte to its left, and setting that as the high-order bit
            -Replace state with new state
            -Use new state in next substitution-permutation network to generate keystream:
                -Perform the same permutation operation with the out-permbox
                -Substitute each byte in the same way using the out-sbox
                -Expand the substituted bytes in the same way
            
        """
    def load_box(self, path):
        box = []
        with open(path, 'r') as f: #not ideal code, but written this way for prototyping. Want this included as part of the program data when in C
            for line in f:
                box.append(int(line))

        return box

    def reset(self):
        self.state = self.inital_state
        self.cache = []
        for i in range(8):
            self.state ^= (self.nonce << 64 * i)

    def _permute(self, state, box): 
        new_state = 0
        for shift in box:
            new_state <<= 1
            new_state |= ((state >> shift)&1)

        return new_state
        
    def _substitute(self, state, box): 
        out_bytes = list(state.to_bytes(32, 'big'))
        for byte_idx in range(32):
            out_bytes[byte_idx] = box[out_bytes[byte_idx]]

        return int.from_bytes(out_bytes, 'big')

    """
    Note: parity check for a byte v can be done with just this code:
    v ^= v >> 4;
    v &= 0xf;
    return (0x6996 >> v) & 1;
    but this seemed like too much of a hack
    """
    def _expand(self, state): 
        in_bytes = list(state.to_bytes(32, 'big')) 
        out_bytes = []
        for byte_idx in range(32): #can get the parity in four steps:
            combined = in_bytes[byte_idx] ^ in_bytes[byte_idx-1]
            combined ^= (combined >> 4) #preserves parity at each step since we're "folding" the byte over itself
            combined ^= (combined >> 2)
            combined ^= (combined >> 1) #TODO clean this up a bit
            out_byte = in_bytes[byte_idx] | ((combined & 1) << 7)
            out_bytes.append(out_byte)
        return int.from_bytes(out_bytes, 'big')

    def getbytes(self, n):

        out_bytes = self.cache[:n]
        n -= len(self.cache)


        #the below code is OLD and i'm rewritting it with the code above
        rounds = ceil(n / 32)

        round_bytes = []
        for r in range(rounds):
            self.state = self._permute(self.state, self.permbox) #optimization note: if we want to gain speed in exchange for bigger code, we can change _substitute
            self.state = self._substitute(self.state, self.sbox) #and following lines to remove redundant to_bytes and from_bytes calls
            self.state = self._expand(self.state)

            perm = self._permute(self.state, self.out_permbox) 
            sub_state = self._substitute(perm, self.out_sbox)
            out_state = self._expand(sub_state)
            round_bytes += list(out_state.to_bytes(32, 'big'))

        #reset cache
        self.cache = round_bytes[n:]
        out_bytes += round_bytes[:n] 

        return out_bytes 



    def getbyte(self):
        
        if len(self.cache) == 0:
            self.state = self._permute(self.state, self.permbox) 
            self.state = self._substitute(self.state, self.sbox)
            self.state = self._expand(self.state)
            
            perm = self._permute(self.state, self.out_permbox) 
            sub_state = self._substitute(perm, self.out_sbox)
            out_state = self._expand(sub_state)
            out_bytes = list(out_state.to_bytes(32, 'big'))
            self.cache = out_bytes[1:] 
            return out_bytes[0]
        
        else:
            out = self.cache[0]
            self.cache = self.cache[1:]
            return out
