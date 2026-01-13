import socket
import pickle
import time


def calculer_score(pieces_restantes, fini_par_unite):
    malus = 0
    for p in pieces_restantes:
        malus -= len(p)
    if len(pieces_restantes) == 0:
        return 20 if fini_par_unite else 15
    return malus


def main_serveur():
    host = '0.0.0.0'
    port = 5556
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(4)

    print("--- Serveur Blokus 4 Joueurs Lancé ---")
    clients = []
    couleurs = ["red", "blue", "green", "yellow"]

    # Connexion des 4 joueurs
    for i in range(4):
        conn, addr = server_socket.accept()
        print(f"Joueur {i + 1} ({couleurs[i]}) connecté.")
        conn.send(pickle.dumps(couleurs[i]))
        clients.append(conn)

    grille = [['_'] * 20 for _ in range(20)]
    bloques = [False] * 4
    inventaires = {c: [] for c in couleurs}
    unite_final = {c: False for c in couleurs}
    tour = 0

    while False in bloques:
        if bloques[tour]:
            tour = (tour + 1) % 4
            continue

        current_color = couleurs[tour]

        # 1. Diffuser l'état à TOUS les joueurs
        for i, conn in enumerate(clients):
            try:
                conn.send(pickle.dumps({
                    "grille": grille,
                    "actif": (i == tour),
                    "coul_actuelle": current_color,
                    "type": "TOUR"
                }))
            except:
                bloques[i] = True

        # 2. Recevoir l'action du joueur actif
        try:
            data = clients[tour].recv(8192)
            if not data: break
            resultat = pickle.loads(data)

            if resultat == "CHANGER":
                continue

            if resultat == "BLOQUER":
                print(f"{current_color} est bloqué.")
                bloques[tour] = True
                # Demande l'inventaire final pour le score
                clients[tour].send(pickle.dumps("REQ_PIECES"))
                inventaires[current_color] = pickle.loads(clients[tour].recv(8192))

            elif isinstance(resultat, dict) and resultat.get("status") == "FINI":
                print(f"{current_color} a TOUT posé !")
                bloques[tour] = True
                unite_final[current_color] = resultat["unite"]
                inventaires[current_color] = []

            else:  # Coordonnées de placement
                for x, y in resultat:
                    grille[y][x] = current_color

                # Mise à jour de l'inventaire pour le score
                clients[tour].send(pickle.dumps("REQ_PIECES"))
                inventaires[current_color] = pickle.loads(clients[tour].recv(8192))

            tour = (tour + 1) % 4
        except:
            bloques[tour] = True
            break

    # --- Scores finaux ---
    res_scores = [calculer_score(inventaires[c], unite_final[c]) for c in couleurs]
    bilan = "FIN DE PARTIE\n" + " | ".join([f"{couleurs[i].upper()}: {res_scores[i]}" for i in range(4)])
    print(bilan)

    for c in clients:
        try:
            c.send(pickle.dumps({"type": "FIN", "msg": bilan}))
        except:
            pass

    server_socket.close()


if __name__ == "__main__":
    main_serveur()
