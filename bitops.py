#Provides helper functions that perform bit fiddling in an efficient way
def rotate_right(word):
    return (word>>1) | ((word & 1) << 63)

def rotate_left(word):
    return (word>>63)| ((word<<1)&0xFFFFFFFFFFFFFFFF)