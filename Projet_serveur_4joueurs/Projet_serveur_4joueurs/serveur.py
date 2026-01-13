import socket
import pickle

def main_serveur():
    host = '0.0.0.0'
    port = 5556
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(4)

    clients = []
    couleurs = ["red", "blue", "green", "yellow"]
    joueurs_en_jeu = [True, True, True, True]
    
    print(f"Serveur lancé sur le port {port}. En attente des joueurs...")

    try:
        # 1. Connexion des 4 joueurs
        while len(clients) < 4:
            conn, addr = server_socket.accept()
            idx = len(clients)
            print(f"Joueur {idx + 1} ({couleurs[idx]}) connecté depuis {addr}")
            conn.send(pickle.dumps(couleurs[idx])) # Envoi de sa couleur
            clients.append(conn)

        grille = [['_'] * 20 for _ in range(20)]
        tour = 0
        en_cours = True

        while en_cours:
            # Vérifier s'il reste des joueurs actifs
            if joueurs_en_jeu.count(True) == 0:
                print("Plus de joueurs actifs. Fin.")
                break

            # Passer le tour si le joueur actuel est bloqué
            if not joueurs_en_jeu[tour]:
                tour = (tour + 1) % 4
                continue

            current_conn = clients[tour]
            current_color = couleurs[tour]

            # DIFFUSION de l'état à tous les clients encore connectés
            etat = {
                "grille": grille,
                "actif": False,
                "couleur_tour": current_color
            }

            for i, conn in enumerate(clients):
                try:
                    etat["actif"] = (i == tour)
                    conn.send(pickle.dumps(etat))
                except:
                    joueurs_en_jeu[i] = False

            # RÉCEPTION de l'action du joueur dont c'est le tour
            try:
                data = current_conn.recv(4096)
                if not data:
                    raise Exception("Déconnexion")

                resultat = pickle.loads(data)

                if resultat == "FINI":
                    print(f"VICTOIRE : {current_color} a gagné !")
                    en_cours = False
                elif resultat == "BLOQUER":
                    print(f"{current_color} est bloqué.")
                    joueurs_en_jeu[tour] = False
                    tour = (tour + 1) % 4
                else: 
                    # On suppose que 'resultat' est une liste de coordonnées [(x,y), ...]
                    for x, y in resultat:
                        grille[y][x] = current_color
                    tour = (tour + 1) % 4

            except Exception as e:
                print(f"Erreur avec le joueur {current_color}: {e}")
                joueurs_en_jeu[tour] = False
                tour = (tour + 1) % 4

    finally:
        # Information de fin et fermeture
        print("Fermeture du serveur...")
        for c in clients:
            try:
                c.send(pickle.dumps("FIN_PARTIE"))
                c.close()
            except:
                pass
        server_socket.close()

if __name__ == "__main__":
    main_serveur()
