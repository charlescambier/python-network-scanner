import socket

# Cible : ton propre ordinateur
target = "127.0.0.1"

print(f"--- Scan des ports de mon PC ({target}) ---")

# Scan port  (1 - 1024)
for port in range(1, 1025):
    # Création du socket (AF_INET = IPv4 (choix IPv6 ou 4), SOCK_STREAM = TCP --> used protocole )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Très important : on met un timeout (délai) court (0.01 seconde)
    # sinon le script mettra des heures à finir si le port est fermé
    s.settimeout(0.01)
    
    # On tente la connexion (connect_ex renvoie un code d'erreur au lieu de planter)
    result = s.connect_ex((target, port))
    
    if result == 0:
        print(f"[+] Port {port} : OUVERT")
    
    s.close()

print("--- Scan terminé ---")


"""

*****************************************
Very fast scan
can scan 100 ports simultany
*****************************************
*****************************************
*****************************************
import socket
from concurrent.futures import ThreadPoolExecutor

target = "127.0.0.1"

def check_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5) # On peut mettre un timeout plus long car on est en parallèle
    if s.connect_ex((target, port)) == 0:
        print(f"Port {port} est OUVERT")
    s.close()

print("Scan ultra-rapide lancé...")
# On lance 100 scans en simultané
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(check_port, range(1, 1025))

print("Terminé !")

**********************************************************************************

"""