import socket
from RSA import generate_keypair, decrypt, encrypt

def receive_data(conn):
    data = conn.recv(1024)
    return data

def send_data(conn, data):
    conn.send(data)

def main():
    host = '127.0.0.1'
    port = 6969

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server listening on port", port)

    conn, addr = server_socket.accept()
    print("Connection from:", addr)

    public_key, private_key = generate_keypair(4)

    print("SERVER: PUBLIC KEY: " + str(public_key) + " PRIVATE KEY: " + str(private_key))

    client_public_key = receive_data(conn).decode()  # Decode bytes to string
    client_public_key = (int(client_public_key.split(',')[0]), int(client_public_key.split(',')[1]))

    send_data(conn, f"{public_key[0]},{public_key[1]}".encode())

    while True:
        encrypted_message = receive_data(conn)
        print("encrypted message: "+ str(list(map(int.from_bytes, encrypted_message.split(b',')))))
        decrypted_message = decrypt(list(map(int.from_bytes, encrypted_message.split(b','))), private_key)
        print("Client:", decrypted_message)

        # Check if the message is to quit the server
        if decrypted_message.decode().strip().lower() == "quit":
            print("Quitting the server...")
            break
#dsa
    conn.close()
    server_socket.close()  # Close the server socket

if __name__ == "__main__":
    main()
