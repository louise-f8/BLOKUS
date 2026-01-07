from class_piece import Pieces
from class_color import colors
import fonctions
import time
import os

def main():
    largeur, hauteur = 16, 16
    grille = [['_'] * largeur for _ in range(hauteur)]
    coins_disponibles = {(0, 0), (0, 15), (15, 0), (15, 15)}

    joueurs_initiaux = [
        Pieces("red"),
        Pieces("blue"),
        Pieces("green"),
        Pieces("yellow")
    ]

    joueurs_actifs = list(joueurs_initiaux)

    premier_tour = {j: True for j in joueurs_initiaux}
    index_joueur = 0

    joueurs_bloques = {j: False for j in joueurs_initiaux}

    while sum(joueurs_bloques.values()) < len(joueurs_initiaux):
        joueur_actuel = joueurs_initiaux[index_joueur]

        # Si le joueur est déjà bloqué, on passe au suivant
        if joueurs_bloques[joueur_actuel]:
            index_joueur = (index_joueur + 1) % len(joueurs_initiaux)
            continue

        os.system('cls' if os.name == 'nt' else 'clear')

        piece, nom_piece = fonctions.choix_piece(joueur_actuel, grille)
        piece_rotations = fonctions.toutes_orientations(piece)

        final_coords = fonctions.placement_interactif(
            grille,
            piece_rotations,
            joueur_actuel,
            premier_tour[joueur_actuel],
            coins_disponibles
        )

        if final_coords == "CHANGER":
            continue

        if final_coords == "BLOQUER":
            print(f"\nLe joueur {joueur_actuel.color.upper()} se déclare bloqué.")
            joueurs_bloques[joueur_actuel] = True
            time.sleep(1)
            index_joueur = (index_joueur + 1) % len(joueurs_initiaux)
            continue

        # Placement de la pièce
        for x, y in final_coords:
            grille[y][x] = getattr(colors.fg, joueur_actuel.color) + '■' + colors.reset
            if (x, y) in coins_disponibles:
                coins_disponibles.remove((x, y))

        premier_tour[joueur_actuel] = False
        # Récupérer la taille de la pièce avant de la supprimer pour le bonus final si besoin
        derniere_piece_posee = piece
        fonctions.supprimer_piece(joueur_actuel, nom_piece)

        # Si le joueur n'a plus de pièces, il est terminé
        if not joueur_actuel.pieces:
            print(f"\nINCROYABLE ! {joueur_actuel.color.upper()} a posé toutes ses pièces !")
            joueurs_bloques[joueur_actuel] = True
            # Stocker si la dernière pièce était le petit carré (1x1) pour le bonus Blokus
            joueur_actuel.fini_par_unite = (len(derniere_piece_posee) == 1)

        index_joueur = (index_joueur + 1) % len(joueurs_initiaux)

    # --- CALCUL DES SCORES (Règles Officielles) ---
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 40)
    print("           FIN DE LA PARTIE             ")
    print("=" * 40)

    scores = {}
    for j in joueurs_initiaux:
        # Chaque carré restant = -1 point
        malus = 0
        for p in j.pieces:
            malus -= len(p)

        score_final = malus

        if not j.pieces:  # Si toutes les pièces sont posées
            if getattr(j, 'fini_par_unite', False):
                score_final = +20  # Bonus si la dernière pièce était le 1x1
            else:
                score_final = +15  # Bonus standard

        scores[j.color] = score_final

    # Tri et affichage
    print("\nCLASSEMENT FINAL :")
    classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for i, (couleur, score) in enumerate(classement, 1):
        print(f"{i}. {couleur.upper()} : {score} points")

if __name__ == "__main__":
    main()