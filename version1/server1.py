import socket  # Module pour les sockets
import subprocess  # Module pour exécuter des scripts

# Configuration réseau et utilisateurs
HOST = "localhost"
PORT = 5000
USERS = {"alice": "pass123", "bob": "pass456"}  # Dictionnaire des utilisateurs/mots de passe

def run_script(script):
    """
    Exécute un script Python et renvoie le résultat ou une erreur.
    """
    try:
        result = subprocess.check_output(["python3", "-c", script], stderr=subprocess.STDOUT, text=True)
        return f"Success: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    except FileNotFoundError:
        return "Error: Python interpréteur non trouvé (vérifiez python3)"

def authenticate(user, password):
    """
    Vérifie les identifiants de l'utilisateur.
    :param user: Nom d'utilisateur
    :param password: Mot de passe
    :return: True si valide, False sinon
    """
    return user in USERS and USERS[user] == password

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Serveur en écoute sur {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")
        
        # Reçoit les données au format "user:password"
        auth_data = client_socket.recv(1024).decode("utf-8")
        try:
            user, password = auth_data.split(":", 1)  # Sépare user et password
            if authenticate(user, password):  # Vérifie les identifiants
                client_socket.send("OK".encode("utf-8"))  # Confirme l'authentification
                script = client_socket.recv(1024).decode("utf-8")  # Reçoit le script
                if script:
                    result = run_script(script)
                    client_socket.send(result.encode("utf-8"))
                else:
                    client_socket.send("Error: Aucun script reçu".encode("utf-8"))
            else:
                client_socket.send("Erreur : Authentification échouée".encode("utf-8"))
        except ValueError:
            client_socket.send("Erreur : Format invalide (attendu user:password)".encode("utf-8"))
        client_socket.close()
