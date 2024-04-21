import math

def factorize(n):
    factors = []
    for i in range(2, n+1):
        while n % i == 0:
            factors.append(i)
            n //= i
    return factors

def factorization_attack(encrypted_message, public_key):
    n, e = public_key
    p, q = factorize(n)
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    decrypted = [chr(pow(char, d, n)) for char in encrypted_message]
    return ''.join(decrypted), (n, d)

if __name__ == "__main__":
    # Example usage
    print("Enter the encrypted message (as a list of integers):")
    encrypted_message = eval(input())
    
    print("Enter the public key (as a tuple n,e):")
    public_key = eval(input())
    
    decrypted_message, private_key = factorization_attack(encrypted_message, public_key)
    print("Decrypted message:", decrypted_message)
    print("Private key:", private_key)
