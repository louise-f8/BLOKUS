from class_piece import Pieces
from class_color import colors
import fonctions
import time


def main():
    largeur, hauteur = 16, 16
    grille = [['_'] * largeur for _ in range(hauteur)]
    # Coins pour une grille 16x16 (0 à 15)
    coins_disponibles = {(0, 0), (0, 15), (15, 0), (15, 15)}

    joueur1 = Pieces("red")
    joueur2 = Pieces("blue")

    # Dictionnaires pour suivre l'état des joueurs
    joueurs = [joueur1, joueur2]
    premier_tour = {joueur1: True, joueur2: True}

    joueur_actuel = joueur1

    while True:
        print(f"\nTour du joueur {joueur_actuel.color}")
        fonctions.afficher_grille(grille)
        fonctions.afficher_pieces_joueur(joueur_actuel)

        piece, nom_piece = fonctions.choix_piece(joueur_actuel, grille)
        piece_rotations = fonctions.toutes_orientations(piece)

        # On passe les infos de validation
        final_coords = fonctions.placement_interactif(
            grille,
            piece_rotations,
            joueur_actuel,
            premier_tour[joueur_actuel],
            coins_disponibles
        )
        if final_coords == "CHANGER":
            print("\nChangement de pièce...")
            time.sleep(0.5)
            continue
        if final_coords == "BLOQUER":
            gagnant = joueur2 if joueur_actuel == joueur1 else joueur1
            print(f"\nLe joueur {joueur_actuel.color} est bloqué !")
            print(f"Félicitations ! Le joueur {gagnant.color} a gagné la partie !")
            break
        
        # Avant de supprimer la pièce, on vérifie si c'est le monomino (1x1)
        if fonctions.est_monomino(piece):
            joueur_actuel.derniere_piece_etait_un_par_un = True
        else:
            joueur_actuel.derniere_piece_etait_un_par_un = False
        
        # Placer la pièce
        for x, y in final_coords:
            grille[y][x] = getattr(colors.fg, joueur_actuel.color) + '■' + colors.reset
            # Si c'était un coin, on le retire des dispos pour les autres
            if (x, y) in coins_disponibles:
                coins_disponibles.remove((x, y))

        # Après le premier placement réussi
        premier_tour[joueur_actuel] = False

        fonctions.supprimer_piece(joueur_actuel, nom_piece)

        # Si le joueur vient de poser sa dernière pièce
        if not joueur_actuel.pieces:
            print(f"\nINCROYABLE ! Le joueur {joueur_actuel.color} a posé toutes ses pièces !")

        if fonctions.fin_jeu(joueur1, joueur2) or fonctions.grille_pleine(grille):
            print("\nFin de la partie !")
            break

    
        print("\n" + "="*30)
        print("      RÉSULTATS FINAUX")
        print("="*30)
        for j in [joueur1, joueur2]:
            final_score = fonctions.calculer_score(j)
            print(f"Joueur {j.color.upper()} : {final_score} points")
        
        joueur_actuel = fonctions.joueur_suivant(joueur_actuel, joueurs)

    # --- FIN DE PARTIE : AFFICHAGE DES SCORES ---
    print("\n" + "="*30)
    print("      SCORES FINAUX")
    print("="*30)
    for j in [joueur1, joueur2]:
        final_score = fonctions.calculer_score(j)
        print(f"Joueur {j.color.upper()} : {final_score} points")
    
    # Déterminer le vainqueur aux points
    s1 = fonctions.calculer_score(joueur1)
    s2 = fonctions.calculer_score(joueur2)
    if s1 > s2:
        print(f"\nLe vainqueur est le joueur {joueur1.color.upper()} !")
    elif s2 > s1:
        print(f"\nLe vainqueur est le joueur {joueur2.color.upper()} !")
    else:
        print("\nÉgalité parfaite !")


if __name__ == "__main__":
    main()

