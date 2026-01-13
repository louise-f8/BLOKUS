import fonctions
from class_piece import Pieces
from class_color import colors
import os
import time


def main():
    # --- CONFIGURATION INITIALE ---
    largeur, hauteur = 16, 16
    grille = [['_'] * largeur for _ in range(hauteur)]
    # Coins pour une grille 16x16 (index 0 et 15)
    coins_disponibles = {(0, 0), (0, 15), (15, 0), (15, 15)}

    joueur1 = Pieces("red")
    joueur2 = Pieces("blue")

    # Initialisation des attributs pour le calcul du score final
    for j in [joueur1, joueur2]:
        j.derniere_piece_etait_un_par_un = False

    joueurs = [joueur1, joueur2]
    # Dictionnaires pour suivre l'état spécifique de chaque joueur
    statut_joueurs = {joueur1: True, joueur2: True}  # True = peut encore jouer
    premier_tour = {joueur1: True, joueur2: True}

    joueur_actuel = joueur1

    # --- BOUCLE PRINCIPALE ---
    # La partie continue tant qu'au moins UN joueur n'est pas bloqué
    while True in statut_joueurs.values():

        # Si le joueur actuel est bloqué, on passe immédiatement au suivant
        if not statut_joueurs[joueur_actuel]:
            joueur_actuel = fonctions.joueur_suivant(joueur_actuel, joueurs)
            continue

        # Affichage du jeu complet (Grille + Pièces disponibles)
        os.system('cls' if os.name == 'nt' else 'clear')
        fonctions.afficher_jeu_complet(grille, joueur_actuel)

        print(f"\n--- TOUR DE : {joueur_actuel.color.upper()} ---")

        # 1. Choix de la pièce
        piece, nom_piece = fonctions.choix_piece(joueur_actuel, grille)
        piece_rotations = fonctions.toutes_orientations(piece)

        # 2. Phase de placement interactif
        final_coords = fonctions.placement_interactif(
            grille,
            piece_rotations,
            joueur_actuel,
            premier_tour[joueur_actuel],
            coins_disponibles
        )

        # 3. Traitement de la décision du joueur
        if final_coords == "CHANGER":
            # On relance la boucle pour le même joueur (il change de pièce)
            continue

        if final_coords == "BLOQUER":
            print(f"\nLe joueur {joueur_actuel.color.upper()} est bloqué !")
            statut_joueurs[joueur_actuel] = False
            time.sleep(1)
            joueur_actuel = fonctions.joueur_suivant(joueur_actuel, joueurs)
            continue

        # 4. Placement validé : Mise à jour de la grille
        # On enregistre si c'est un monomino pour le bonus final
        joueur_actuel.derniere_piece_etait_un_par_un = (len(piece) == 1)

        for x, y in final_coords:
            grille[y][x] = getattr(colors.fg, joueur_actuel.color) + '■' + colors.reset
            # Si on pose sur un coin au premier tour, il n'est plus "disponible"
            if (x, y) in coins_disponibles:
                coins_disponibles.remove((x, y))

        # 5. Mise à jour de l'inventaire et du statut
        premier_tour[joueur_actuel] = False
        fonctions.supprimer_piece(joueur_actuel, nom_piece)

        # Si le joueur n'a plus de pièces, il a fini (considéré comme bloqué)
        if not joueur_actuel.pieces:
            print(f"\nINCROYABLE ! Le joueur {joueur_actuel.color.upper()} a tout posé !")
            statut_joueurs[joueur_actuel] = False
            time.sleep(1)

        # Passage au joueur suivant
        joueur_actuel = fonctions.joueur_suivant(joueur_actuel, joueurs)

    # --- FIN DE LA PARTIE ---
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "!" * 40)
    print("        TOUT LE MONDE EST BLOQUÉ ")
    print("!" * 40)

    fonctions.afficher_grille(grille)

    print("\n" + "=" * 35)
    print("         SCORES FINAUX")
    print("   (Malus par carré non posé)")
    print("=" * 35)

    s1 = fonctions.calculer_score(joueur1)
    s2 = fonctions.calculer_score(joueur2)

    print(f" Joueur {joueur1.color.upper():<7} : {s1:>3} points")
    print(f" Joueur {joueur2.color.upper():<7} : {s2:>3} points")
    print("-" * 35)

    if s1 > s2:
        print(f" VICTOIRE DE : {joueur1.color.upper()} !")
    elif s2 > s1:
        print(f" VICTOIRE DE : {joueur2.color.upper()} !")
    else:
        print(" ÉGALITÉ PARFAITE !")

    print("=" * 35)
    input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main()
