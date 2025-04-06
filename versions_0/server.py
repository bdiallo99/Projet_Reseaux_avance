import socket
import subprocess

HOST = "localhost"
PORT = 5000

def run_script(script):
    try:
        # Utiliser 'python3' au lieu de 'python'
        result = subprocess.check_output(["python3", "-c", script], stderr=subprocess.STDOUT, text=True)
        return f"Success: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    except FileNotFoundError:
        return "Error: Python interpréteur non trouvé (vérifiez python3)"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Serveur en écoute sur {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")
        
        data = client_socket.recv(1024).decode("utf-8")
        if data:
            result = run_script(data)
            client_socket.send(result.encode("utf-8"))
        else:
            client_socket.send("Error: Aucun script reçu".encode("utf-8"))
        client_socket.close()
