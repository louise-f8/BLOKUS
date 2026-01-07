import socket
import pickle
import time
from class_pieces import Pieces


def calculer_score(couleur, pieces_restantes, fini_par_unite):
    # Chaque carré non posé = -1 point
    malus = 0
    for p in pieces_restantes:
        malus -= len(p)

    if len(pieces_restantes) == 0:
        if fini_par_unite:
            return 20  # Bonus spécial 1x1
        return 15  # Bonus standard
    return malus


def main_serveur():
    host = '0.0.0.0'
    port = 5556
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))
    server_socket.listen(2)

    print("--- Serveur Blokus Lancé ---")
    print(f"En attente sur le port {port}...")

    try:
        conn1, addr1 = server_socket.accept()
        print(f"Joueur 1 (RED) connecté : {addr1}")
        conn1.send(pickle.dumps("red"))

        conn2, addr2 = server_socket.accept()
        print(f"Joueur 2 (BLUE) connecté : {addr2}")
        conn2.send(pickle.dumps("blue"))


        grille = [['_'] * 16 for _ in range(16)]
        clients = [conn1, conn2]


        couleurs = ["red", "blue"]

        # État global du jeu
        bloques = [False, False]
        inventaires = {"red": [], "blue": []}
        unite_final = {"red": False, "blue": False}
        tour = 0

        while False in bloques:
            if bloques[tour]:
                tour = (tour + 1) % 2
                continue

            current_conn = clients[tour]
            current_color = couleurs[tour]
            other_conn = clients[(tour + 1) % 2]

            # 1. Envoyer l'état au joueur actif
            try:
                current_conn.send(pickle.dumps({"grille": grille, "actif": True, "type": "TOUR"}))
                other_conn.send(pickle.dumps({"grille": grille, "actif": False, "type": "TOUR"}))
            except:
                break

            # 2. Recevoir l'action
            try:
                data = current_conn.recv(4096)
                if not data: break
                resultat = pickle.loads(data)

                if resultat == "CHANGER":
                    continue

                if resultat == "BLOQUER":
                    print(f"Action : {current_color} s'est déclaré bloqué.")
                    bloques[tour] = True

                elif isinstance(resultat, dict) and resultat.get("status") == "FINI":
                    print(f"Action : {current_color} a posé TOUTES ses pièces !")
                    bloques[tour] = True
                    unite_final[current_color] = resultat["unite"]
                    inventaires[current_color] = []

                else:  # Réception de coordonnées
                    print(f"Action : {current_color} a placé une pièce.")
                    for x, y in resultat:
                        grille[y][x] = current_color

                    # On demande l'inventaire mis à jour pour le score en cas de déco
                    current_conn.send(pickle.dumps("REQ_PIECES"))
                    inventaires[current_color] = pickle.loads(current_conn.recv(4096))

                tour = (tour + 1) % 2
            except:
                break

        # --- Fin de partie et scores ---
        score_red = calculer_score("red", inventaires["red"], unite_final["red"])
        score_blue = calculer_score("blue", inventaires["blue"], unite_final["blue"])

        bilan = f"FIN DE PARTIE\nScores : RED = {score_red} | BLUE = {score_blue}"
        print(bilan)

        for c in clients:
            try:
                c.send(pickle.dumps({"type": "FIN", "msg": bilan}))
            except:
                pass

    except KeyboardInterrupt:
        print("\nArrêt manuel.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main_serveur()

