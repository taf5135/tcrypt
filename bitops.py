#Provides helper functions that perform bit fiddling in an efficient way

def rotate_left(word, amt, size=64):
    return (word << amt)|(word >> (size-amt)) #TODO test this, needs an & with the size

def rotate_right(word, amt, size=64):
    return (word >> amt )|(word << (size-amt)) #TODO test this