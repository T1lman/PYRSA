import socket
from RSA import generate_keypair, encrypt, decrypt

def receive_data(conn):
    data = conn.recv(1024)
    return data

def send_data(conn, data):
    conn.send(data)

def main():
    host = '127.0.0.1'
    port = 6969

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    public_key, private_key = generate_keypair(4)
    print("CLIENT: PUBLIC KEY: " + str(public_key) + " PRIVATE KEY: " + str(private_key))
    send_data(client_socket, f"{public_key[0]},{public_key[1]}".encode())

    server_public_key = receive_data(client_socket).decode()  # Decode bytes to string
    server_public_key = (int(server_public_key.split(',')[0]), int(server_public_key.split(',')[1]))
    print("SERVER: PUBLIC KEY: " + str(server_public_key) )
    while True:
        # Custom message input
        message = input("Client: ")
        encrypted_message = encrypt(message, server_public_key)
        print("encrypted message: " + str(encrypted_message))
        send_data(client_socket, b','.join(map(int.to_bytes, encrypted_message, [8]*len(encrypted_message))))

    client_socket.close()

if __name__ == "__main__":
    main()
