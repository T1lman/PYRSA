import random
import math

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as d*2^r + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime(length=1024):
    while True:
        p = generate_prime_candidate(length)
        if is_prime(p):
            return p

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_keypair(length=1024):
    p = generate_prime(length)
    
    # Generate q until it's distinct from p
    while True:
        q = generate_prime(length)
        if q != p:
            break
    
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2, phi)
        if math.gcd(e, phi) == 1:
            break

    d = modinv(e, phi)
    return (n, e), (n, d)


def encrypt(message, public_key):
    n, e = public_key
    encrypted = []
    for char in message:
        # Check if character is within valid ASCII range
        if ord(char) > 127:
            raise ValueError("Message contains characters outside ASCII range (0-127).")
        encrypted.append(pow(ord(char), e, n))
    return encrypted


def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted = [pow(char, d, n).to_bytes((pow(char, d, n).bit_length() + 7) // 8, 'big') for char in encrypted_message]
    return b''.join(decrypted)



if __name__ == "__main__":
    # Test
    public_key, private_key = generate_keypair(16)
    message = "Hello, RSA!"
    encrypted_message = encrypt(message, public_key)
    decrypted_message = decrypt(encrypted_message, private_key)

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)
