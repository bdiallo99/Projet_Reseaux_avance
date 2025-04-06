import socket

HOST = "localhost"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    script = input("Entrez un script Python : ")
    client_socket.send(script.encode("utf-8"))
    
    result = client_socket.recv(1024).decode("utf-8")
    print("Résultat :", result)
