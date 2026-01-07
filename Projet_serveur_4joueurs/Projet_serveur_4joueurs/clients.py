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

    try:
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


    # Blokus 4 joueurs = Grille de 20 (index 0 à 19)
    coins_dispo_locaux = {(0, 0), (0, 19), (19, 0), (19, 19)}

    je_suis_bloque = False  # Pour savoir si on attend juste la fin

    while True:
        try:
            data = client_socket.recv(8192)
            message = pickle.loads(data)
            if not data:
                print("\nConnexion perdue avec le serveur.")
                break


            if message == "VICTOIRE" or message == "BRAVO_GAGNE":
                print("\n" + "*" * 40)
                print("   FÉLICITATIONS ! VOUS AVEZ GAGNÉ !   ")
                print("*" * 40)
                break

            if message == "DEFAITE":
                print("\n" + "x" * 40)
                print("   DOMMAGE... VOUS AVEZ PERDU.   ")
                print("x" * 40)
                break

            if message == "FIN_PARTIE":
                score_final = fonctions.calculer_score(mon_joueur)
                print("\n" + "="*30)
                print(f"      PARTIE TERMINÉE")
                print(f"      VOTRE SCORE : {score_final} pts")
                print("="*30)
                break


            state = message
            grille = state["grille"]
            mon_tour = state["actif"]
            couleur_actuelle = state.get("couleur_tour", "Inconnue")

        except Exception as e:
            print(f"\nErreur de réception : {e}")
            break

        grille_a_afficher = fonctions.formater_grille_couleurs(grille)
        os.system('cls' if os.name == 'nt' else 'clear')


        if not mon_tour:
            fonctions.afficher_grille(grille_a_afficher)
            if je_suis_bloque:
                print(f"\n[{ma_couleur.upper()}] Vous êtes BLOQUÉ. Observation de la partie...")
            else:
                print(f"\n[{ma_couleur.upper()}] Attente de : {couleur_actuelle.upper()}...")
            continue


        if not je_suis_bloque:
            print(f"--- TOUR DE : {ma_couleur.upper()} ---")
            # Cette fonction utilise maintenant la version avec score en temps réel
            fonctions.afficher_jeu_complet(grille_a_afficher, mon_joueur)

        print(f"--- TOUR DE : {ma_couleur.upper()} ---")
        fonctions.afficher_grille(grille_a_afficher)
        fonctions.afficher_pieces_joueur(mon_joueur)

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
            je_suis_bloque = True
            print("\nVous avez déclaré être bloqué. Attente des autres...")
        else:
            fonctions.supprimer_piece(mon_joueur, nom_piece)
            est_premier_tour = False

            if len(mon_joueur.pieces) == 0:
                print("\nINCROYABLE ! Vous avez posé toutes vos pièces !")
                client_socket.send(pickle.dumps("FINI"))
                # On ne break pas tout de suite pour attendre le message de victoire du serveur
            else:
                client_socket.send(pickle.dumps(final_coords))

    client_socket.close()
    input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main_client()