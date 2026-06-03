import random
import string

def generate_short_code(length=6):
    #created the pool of characters (A-Z,a-z,0-9)
    characters=string.ascii_letters + string.digits 
    #created the short code by choosing random characters from the pool for the given length
    return''.join(random.choice(characters) for _ in range(length))


