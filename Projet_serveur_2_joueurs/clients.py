import socket
import pickle
import fonctions
from class_pieces import Pieces
import os
import time


def main_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 5556))
    except Exception as e:
        print(f"Impossible de se connecter au serveur : {e}")
        return

    try:  # Recevoir couleur
        data_couleur = client_socket.recv(1024)
        if not data_couleur:
            return
        ma_couleur = pickle.loads(data_couleur)
        print(f"Vous jouez les : {ma_couleur}")
    except:
        print("Erreur lors de l'attribution de la couleur.")
        return

    mon_joueur = Pieces(ma_couleur)
    est_premier_tour = True
    coins_dispo_locaux = {(0, 0), (0, 15), (15, 0), (15, 15)}

    while True:
        try:  # etat du serveur
            data = client_socket.recv(8192)
            if not data:
                print("\nConnexion perdue avec le serveur.")
                break

            message = pickle.loads(data)

            # --- NOUVEAUTÉ : Répondre à la demande d'inventaire du serveur ---
            if message == "REQ_PIECES":
                client_socket.send(pickle.dumps(mon_joueur.pieces))
                continue

            # --- NOUVEAUTÉ : Gérer l'affichage de fin de partie ---
            if isinstance(message, dict) and message.get("type") == "FIN":
                print("\n" + "=" * 40)
                print(message["msg"])
                print("=" * 40)
                break

            if message == "ABANDON":
                print("\n" + "!" * 40)
                print("L'ADVERSAIRE A QUITTÉ LA PARTIE !")
                print("Victoire par forfait.")
                print("!" * 40)
                break

            # Extraction des données de jeu normales
            state = message
            grille = state["grille"]
            mon_tour = state["actif"]

        except Exception as e:
            print(f"\nErreur de réception : {e}")
            break

        grille_a_afficher = fonctions.formater_grille_couleurs(grille)

        if not mon_tour:
            os.system('cls' if os.name == 'nt' else 'clear')
            fonctions.afficher_grille(grille_a_afficher)
            print(f"\n[{ma_couleur.upper()}] Attente de l'autre joueur...")
            continue

        # --- PHASE DE JEU ACTIVE ---
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"--- TOUR DE : {ma_couleur.upper()} ---")
        fonctions.afficher_jeu_complet(grille_a_afficher, mon_joueur)

        piece, nom_piece = fonctions.choix_piece(mon_joueur, grille_a_afficher)
        piece_rotations = fonctions.toutes_orientations(piece)

        final_coords = fonctions.placement_interactif(
            grille_a_afficher,
            piece_rotations,
            mon_joueur,
            est_premier_tour,
            coins_dispo_locaux
        )

        if final_coords == "CHANGER":
            client_socket.send(pickle.dumps("CHANGER"))
            continue

        if final_coords == "BLOQUER":
            client_socket.send(pickle.dumps("BLOQUER"))
            print("\nVous avez déclaré être bloqué. Attente de la fin de partie...")
            # On ne sort pas de la boucle, on attend le message "FIN" du serveur
            continue

        else:
            # Sauvegarder la taille pour le bonus de fin
            taille_piece = len(piece)
            fonctions.supprimer_piece(mon_joueur, nom_piece)
            est_premier_tour = False

            if len(mon_joueur.pieces) == 0:
                print("\nINCROYABLE ! Vous avez posé toutes vos pièces !")
                # On envoie un dictionnaire pour le bonus 1x1
                client_socket.send(pickle.dumps({
                    "status": "FINI",
                    "unite": (taille_piece == 1)
                }))
                # On attend le message de fin du serveur pour voir les scores
            else:
                client_socket.send(pickle.dumps(final_coords))

    client_socket.close()
    print("\nPartie terminée.")


if __name__ == "__main__":
    main_client()