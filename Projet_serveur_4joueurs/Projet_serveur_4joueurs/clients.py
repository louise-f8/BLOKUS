import socket
import pickle
import fonctions
from class_pieces import Pieces
import os


def main_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 5556))
    except Exception as e:
        print(f"Erreur connexion : {e}");
        return

    ma_couleur = pickle.loads(client_socket.recv(1024))
    print(f"Vous jouez les : {ma_couleur}")
    mon_joueur = Pieces(ma_couleur)
    est_premier_tour = True
    coins_dispo_locaux = {(0, 0), (0, 19), (19, 0), (19, 19)}
    je_suis_bloque = False

    while True:
        try:
            data = client_socket.recv(8192)
            if not data:
                print("Connexion perdue avec le serveur")
                break
            message = pickle.loads(data)

            # Le serveur demande les pièces pour le score
            if message == "REQ_PIECES":
                client_socket.send(pickle.dumps(mon_joueur.pieces))
                continue

            # Fin de partie
            if isinstance(message, dict) and message.get("type") == "FIN":
                print("\n" + "=" * 40 + "\n" + message["msg"] + "\n" + "=" * 40)
                break

            grille_aff = fonctions.formater_grille_couleurs(message["grille"])
            mon_tour = message["actif"]
            coul_actuelle = message.get("coul_actuelle", "???")

            if not mon_tour:
                os.system('cls' if os.name == 'nt' else 'clear')
                fonctions.afficher_grille(grille_aff)
                if je_suis_bloque:
                    print(f"\n[{ma_couleur.upper()}] Vous êtes BLOQUÉ. Attente de la fin...")
                else:
                    print(f"\n[{ma_couleur.upper()}] Attente de : {coul_actuelle.upper()}...")
                continue

            if je_suis_bloque:
                client_socket.send(pickle.dumps("BLOQUER"))
                continue

            # PHASE ACTIVE
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"--- TOUR DE : {ma_couleur.upper()} ---")
            fonctions.afficher_jeu_complet(grille_aff, mon_joueur)

            piece, nom_piece = fonctions.choix_piece(mon_joueur, grille_aff)

            final_coords = fonctions.placement_interactif(
                grille_aff,
                fonctions.toutes_orientations(piece),
                mon_joueur,
                est_premier_tour,
                coins_dispo_locaux
            )

            if final_coords == "CHANGER":
                client_socket.send(pickle.dumps("CHANGER"))
            elif final_coords == "BLOQUER":
                je_suis_bloque = True
                client_socket.send(pickle.dumps("BLOQUER"))
            else:
                taille = len(piece)
                fonctions.supprimer_piece(mon_joueur, nom_piece)
                est_premier_tour = False
                if len(mon_joueur.pieces) == 0:
                    client_socket.send(pickle.dumps({"status": "FINI", "unite": (taille == 1)}))
                else:
                    client_socket.send(pickle.dumps(final_coords))

        except Exception as e:
            print(f"Erreur : {e}");
            break

    client_socket.close()


if __name__ == "__main__":
    main_client()
