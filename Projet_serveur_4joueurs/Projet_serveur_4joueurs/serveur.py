import socket
import pickle


def main_serveur():
    host = '0.0.0.0'
    port = 5556
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(4)

    print("\nPartie terminée. Envoi des résultats...")
    # Ici, vous pourriez demander aux clients leurs scores ou les calculer si le serveur suivait les pièces.
    # Pour faire simple avec votre structure actuelle, on informe les clients que c'est la FIN.
    for conn in clients:
        try:
            conn.send(pickle.dumps("FIN_PARTIE"))
        except:
            pass

    clients = []
    couleurs = ["red", "blue", "green", "yellow"]
    joueurs_en_jeu = [True, True, True, True]

    try:
        for i in range(4):
            conn, addr = server_socket.accept()
            print(f"Joueur {i + 1} ({couleurs[i]}) connecté.")
            conn.send(pickle.dumps(couleurs[i]))
            clients.append(conn)

        grille = [['_'] * 20 for _ in range(20)]
        tour = 0
        en_cours = True

        while en_cours:
            # --- 1. COMPTER LES JOUEURS RESTANTS ---
            nb_restants = joueurs_en_jeu.count(True)

            # Si un seul joueur reste en lice, il a gagné par forfait des autres
            if nb_restants == 1:
                index_gagnant = joueurs_en_jeu.index(True)
                couleur_gagnante = couleurs[index_gagnant]
                print(f"VICTOIRE PAR SURVIE : {couleur_gagnante} est le dernier à pouvoir jouer !")

                for i, conn in enumerate(clients):
                    msg = "VICTOIRE" if i == index_gagnant else "DEFAITE"
                    try:
                        conn.send(pickle.dumps(msg))
                    except:
                        pass
                break

            # Si tout le monde est bloqué en même temps (rare)
            if nb_restants == 0:
                print("Égalité : tout le monde est bloqué.")
                break

            # --- 2. PASSER LE TOUR DES JOUEURS BLOQUÉS ---
            if not joueurs_en_jeu[tour]:
                tour = (tour + 1) % 4
                continue

            current_conn = clients[tour]
            current_color = couleurs[tour]

            # --- 3. DIFFUSION DE L'ÉTAT ---
            for i, conn in enumerate(clients):
                try:
                    etat = {
                        "grille": grille,
                        "actif": (i == tour),
                        "couleur_tour": current_color
                    }
                    conn.send(pickle.dumps(etat))
                except:
                    joueurs_en_jeu[i] = False

            # --- 4. RÉCEPTION DE L'ACTION ---
            try:
                data = current_conn.recv(4096)
                if not data:
                    joueurs_en_jeu[tour] = False
                    tour = (tour + 1) % 4
                    continue

                resultat = pickle.loads(data)


                if resultat == "FINI":  # Le joueur a posé TOUTES ses pièces
                    print(f"FINI : {current_color} a vidé sa main !")
                    en_cours = False
                    break

                elif resultat == "BLOQUER":
                    print(f"{current_color} est bloqué.")
                    joueurs_en_jeu[tour] = False
                    if joueurs_en_jeu.count(True) == 0:
                        en_cours = False
                        break
                    tour = (tour + 1) % 4

                elif resultat == "CHANGER":
                    continue

                else:  # Placement de pièce
                    for x, y in resultat:
                        grille[y][x] = current_color
                    tour = (tour + 1) % 4

            except:
                joueurs_en_jeu[tour] = False
                tour = (tour + 1) % 4

    finally:
        for c in clients: c.close()
        server_socket.close()