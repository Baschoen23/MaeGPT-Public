import random
import string



def generate_string(length=16):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

#print(generate_string())



'''
def generate_string():
    session_id = (random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16))
    uniqueDBKey= ""
    for ch in session_id:
        uniqueDBKey += ''.join(ch)
    return uniqueDBKey
print(generate_string())
'''