from class_color import colors
import os
import copy
import readchar
import time

def afficher_grille(grille):
    hauteur=len(grille)
    largeur=len(grille[0])
    print("    ", end="")
    for col in range(1, largeur + 1):
        print(f"{col:2}", end=" ")
    print()
    # Lignes de la grille
    for i in range(hauteur):
        # Numéro de ligne
        print(f"{i + 1:2}  ", end=" ")

        for j in range(largeur):
            print(grille[i][j], end="  ")
        print()

# Rotation 90° horaire
def rotation_90(piece):
    p = [(y, -x) for (x, y) in piece]

    # Recentrer à (0,0)
    min_x = min(x for x, y in p)
    min_y = min(y for x, y in p)

    return [(x - min_x, y - min_y) for (x, y) in p]

# Miroir horizontal
def rotation_miroir(piece):
    p = [(-x, y) for (x, y) in piece]

    # Recentrer à (0,0)
    min_x = min(x for x, y in p)
    min_y = min(y for x, y in p)

    return [(x - min_x, y - min_y) for (x, y) in p]

# liste de toutes les orientations possible de la pièce
def toutes_orientations(piece):
    orientations = []

    # Pièce normale puis rotation de 90°
    p = piece
    for _ in range(4):
        p_triee = sorted(p)
        if p_triee not in orientations:
            orientations.append(p_triee)
        p = rotation_90(p)

    # Pièce en miroir vertical puis horizontal
    p = rotation_miroir(piece)
    for _ in range(4):
        p_triee = sorted(p)
        if p_triee not in orientations:
            orientations.append(p_triee)
        p = rotation_90(p)

    return orientations

# demander au joueur quelle orientation le joueur choisit

def afficher_pieces_joueur(joueur):
    print(f"Pièces du joueur {joueur.color} :")
    for i, piece in enumerate(joueur.pieces, start=1):
        print(f"Pièce {i}")
        afficher_piece(piece, joueur)
        print()

def afficher_piece(piece, joueur):
    couleur = getattr(colors.fg, joueur.color)

    max_x = max(p[0] for p in piece)
    max_y = max(p[1] for p in piece)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in piece:
                print(couleur + "■ " + colors.reset, end=" ")
            else:
                print("  ", end=" ")
        print()

def choix_piece(joueur, grille):
    choix_possibles = [f"P{i + 1}" for i in range(len(joueur.pieces))]

    while True:
        # 1. On nettoie l'écran
        os.system('cls' if os.name == 'nt' else 'clear')

        # 2. On affiche la grille actuelle et les pièces à côté
        # Note : on passe la grille telle quelle (déjà formatée avec les couleurs)
        afficher_jeu_complet(grille, joueur)

        print(f"\nC'est au tour du joueur {joueur.color.upper()}")
        choix = input(
            f"Choisissez une pièce parmi les disponibles ({choix_possibles[0]}-{choix_possibles[-1]}) : ").upper().strip()

        if choix in choix_possibles:
            index = int(choix[1:]) - 1
            piece_finale = joueur.pieces[index]
            return piece_finale, choix
        else:
            print("Choix invalide ! Appuyez sur Entrée pour réessayer.")
            input()

def supprimer_piece(joueur,choix):
    if choix=='P1':
        joueur.pieces.pop(0)
    elif choix=='P2':
        joueur.pieces.pop(1)
    elif choix=='P3':
        joueur.pieces.pop(2)
    elif choix=='P4':
        joueur.pieces.pop(3)
    elif choix=='P5':
        joueur.pieces.pop(4)
    elif choix=='P6':
        joueur.pieces.pop(5)
    elif choix=='P7':
        joueur.pieces.pop(6)
    elif choix=='P8':
        joueur.pieces.pop(7)
    elif choix=='P9':
        joueur.pieces.pop(8)
    elif choix=='P10':
        joueur.pieces.pop(9)
    elif choix=='P11':
        joueur.pieces.pop(10)
    elif choix=='P12':
        joueur.pieces.pop(11)
    elif choix=='P13':
        joueur.pieces.pop(12)
    elif choix=='P14':
        joueur.pieces.pop(13)
    elif choix=='P15':
        joueur.pieces.pop(14)
    elif choix=='P16':
        joueur.pieces.pop(15)
    elif choix=='P17':
        joueur.pieces.pop(16)
    elif choix=='P18':
        joueur.pieces.pop(17)
    elif choix=='P19':
        joueur.pieces.pop(18)
    elif choix=='P20':
        joueur.pieces.pop(19)
    elif choix=='P21':
        joueur.pieces.pop(20)
    return joueur.pieces

def placement_valide(piece_finale, grille, joueur, est_premier_tour, coins_disponibles):
    contact_diagonale = False
    touche_coin = False
    couleur_joueur = getattr(colors.fg, joueur.color) + '■' + colors.reset

    for x, y in piece_finale:
        # 1. Vérifier les limites de la grille
        if not (0 <= x < len(grille[0]) and 0 <= y < len(grille)):
            return False

        # 2. Vérifier si la case est libre
        if grille[y][x] != '_':
            return False

        # 3. Premier tour : doit toucher un coin disponible
        if est_premier_tour:
            if (x, y) in coins_disponibles:
                touche_coin = True

        # 4. Tours suivants : Vérifier adjacence (interdit) et diagonale (obligatoire)
        else:
            adjacents = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for ax, ay in adjacents:
                if 0 <= ax < len(grille[0]) and 0 <= ay < len(grille):
                    if grille[ay][ax] == couleur_joueur:
                        return False  # Interdit de toucher par les côtés

            diagonales = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
            for dx, dy in diagonales:
                if 0 <= dx < len(grille[0]) and 0 <= dy < len(grille):
                    if grille[dy][dx] == couleur_joueur:
                        contact_diagonale = True

    if est_premier_tour:
        return touche_coin
    return contact_diagonale


def fin_jeu(joueur1, joueur2):
    fin_jeu=False
    if joueur1.pieces == [] or joueur2.pieces == []:
        fin_jeu=True
    return fin_jeu

def grille_pleine(grille):
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == '_':
                return False
    return True

def joueur_suivant(joueur_actuel, liste_joueurs):
    index = liste_joueurs.index(joueur_actuel)
    index_suivant = (index + 1) % len(liste_joueurs)
    return liste_joueurs[index_suivant]


def afficher_grille_interactive(grille, piece, position, joueur):
    temp_grille = copy.deepcopy(grille)
    px0, py0 = position
    for dx, dy in piece:
        x, y = px0 + dx, py0 + dy
        if 0 <= x < len(temp_grille[0]) and 0 <= y < len(temp_grille):
            temp_grille[y][x] = getattr(colors.fg, joueur.color) + '■' + colors.reset
    os.system('cls' if os.name == 'nt' else 'clear')
    afficher_grille(temp_grille)


def placement_interactif(grille, piece_rotations, joueur, est_premier_tour, coins_disponibles):
    piece_index = 0
    piece = piece_rotations[piece_index]
    position = [0, 0]  # position initiale

    while True:
        afficher_grille_interactive(grille, piece, position, joueur)
        print(f"\nJoueur {joueur.color}")
        print("Flèches: Déplacer | Espace: Tourner | Entrée: Valider | 'q': Choisir une autre pièce | 'p': Plus de pièce plaçable")

        key = readchar.readkey()

        if key.lower() == 'q':
            return "CHANGER"
        if key.lower() == 'p':
            return "BLOQUER"

        if key == readchar.key.UP:
            position[1] = max(0, position[1] - 1)
        elif key == readchar.key.DOWN:
            position[1] = min(len(grille) - 1, position[1] + 1)
        elif key == readchar.key.LEFT:
            position[0] = max(0, position[0] - 1)
        elif key == readchar.key.RIGHT:
            position[0] = min(len(grille[0]) - 1, position[0] + 1)
        elif key == readchar.key.SPACE:
            piece_index = (piece_index + 1) % len(piece_rotations)
            piece = piece_rotations[piece_index]
        elif key == readchar.key.ENTER:
            final_coords = [(position[0] + dx, position[1] + dy) for dx, dy in piece]
            # Vérification que toutes les cases sont libres et dans la grille
            if placement_valide(final_coords, grille, joueur, est_premier_tour, coins_disponibles):
                return final_coords
            else:
                print("Placement invalide ! Appuyez sur une touche pour recommencer.")
                readchar.readkey()
        time.sleep(0.05)  # pause pour limiter la vitesse de lecture des touches

def formater_grille_couleurs(grille_brute):
    """Transforme les noms de couleurs en carrés colorés (4 couleurs)"""
    nouvelle_grille = [ligne[:] for ligne in grille_brute]
    mapping = {
        'red': colors.fg.red,
        'blue': colors.fg.blue,
        'green': colors.fg.green,
        'yellow': colors.fg.yellow
    }
    for y in range(len(nouvelle_grille)):
        for x in range(len(nouvelle_grille[0])):
            val = nouvelle_grille[y][x]
            if val in mapping:
                nouvelle_grille[y][x] = mapping[val] + '■' + colors.reset
    return nouvelle_grille

def afficher_jeu_complet(grille, joueur):
    # 1. On prépare le visuel des pièces à droite
    visuel_droite = generer_visuel_pieces(joueur)

    # 2. On prépare les lignes de la grille à gauche
    lignes_grille = []
    largeur = len(grille[0])

    # Entête de la grille (numéros de colonnes)
    entete = "    " + "".join([f"{col:2} " for col in range(1, largeur + 1)])
    lignes_grille.append(entete)

    for i in range(len(grille)):
        ligne_txt = f"{i + 1:2}  " + "  ".join(grille[i])
        lignes_grille.append(ligne_txt)

    # 3. Affichage combiné
    print("\n" + "=" * 80)  # Séparateur visuel

    # On itère sur le maximum de lignes entre les deux colonnes
    nb_lignes = max(len(lignes_grille), len(visuel_droite))

    for i in range(nb_lignes):
        # On prend la ligne de gauche ou du vide si fini
        gauche = lignes_grille[i] if i < len(lignes_grille) else " " * len(lignes_grille[0])
        # On ajoute un séparateur central
        separateur = "  |  "
        # On prend la ligne de droite ou du vide si fini
        droite = visuel_droite[i] if i < len(visuel_droite) else ""

        print(f"{gauche}{separateur}{droite}")

def generer_visuel_pieces(joueur, pieces_par_ligne=8):
    lignes_finales = [f"--- PIÈCES DISPONIBLES ({joueur.color.upper()}) ---", ""]
    couleur = getattr(colors.fg, joueur.color)

    # On traite les pièces par blocs (ex: de 3 en 3)
    for i in range(0, len(joueur.pieces), pieces_par_ligne):
        groupe = joueur.pieces[i: i + pieces_par_ligne]
        indices = range(i + 1, i + len(groupe) + 1)

        # 1. On prépare les étiquettes (P1, P2, P3...)
        etiquettes = ""
        for idx in indices:
            etiquettes += f"P{idx:<10}"  # Espace constant entre les noms
        lignes_finales.append(etiquettes)

        # 2. On dessine les formes du groupe ligne par ligne
        # On suppose une hauteur max de 5 pour les pièces Blokus
        for y in range(5):
            ligne_cumulee = ""
            for p in groupe:
                # Dessin d'une pièce
                forme_txt = ""
                for x in range(5):
                    if (x, y) in p:
                        forme_txt += couleur + "■ " + colors.reset
                    else:
                        forme_txt += "  "
                ligne_cumulee += forme_txt + " "  # Espace entre deux pièces
            lignes_finales.append(ligne_cumulee)

        lignes_finales.append("")  # Espace entre les rangées

    return lignes_finales
