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
    # On crée une copie profonde pour ne pas modifier la vraie grille pendant la prévisualisation
    temp_grille = copy.deepcopy(grille)
    px0, py0 = position
    couleur_pion = getattr(colors.fg, joueur.color) + '■' + colors.reset

    for dx, dy in piece:
        x, y = px0 + dx, py0 + dy
        if 0 <= x < len(temp_grille[0]) and 0 <= y < len(temp_grille):
            # On place le symbole avec le même format que dans la grille réelle
            temp_grille[y][x] = couleur_pion

    os.system('cls' if os.name == 'nt' else 'clear')
    # Utiliser la fonction globale pour garantir que l'alignement est le même que lors du choix de pièce
    afficher_jeu_complet(temp_grille, joueur)


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
        time.sleep(0.05)# pause pour limiter la vitesse de lecture des touches


def generer_visuel_pieces(joueur, pieces_par_ligne=7):
    # Calcul du score actuel (carrés posés)
    score_actuel = 89 - sum(len(p) for p in joueur.pieces)
    
    lignes_finales = [
        f" --- PIÈCES DISPONIBLES ({joueur.color.upper()}) ---",
        f" SCORE ACTUEL : {score_actuel} pts",
        ""
    ]
    couleur = getattr(colors.fg, joueur.color)
    LARGEUR_BLOC = 12 # Espace horizontal pour chaque bloc de pièce

    for i in range(0, len(joueur.pieces), pieces_par_ligne):
        groupe = joueur.pieces[i: i + pieces_par_ligne]
        
        # 1. Ligne des noms (P1, P2...)
        ligne_noms = ""
        for j in range(len(groupe)):
            nom = f"P{i + j + 1}"
            ligne_noms += f"{nom:<{LARGEUR_BLOC}}"
        lignes_finales.append(ligne_noms)

        # 2. Dessin des formes (5 lignes de haut)
        for y in range(5):
            ligne_formes = ""
            for p in groupe:
                str_piece = ""
                for x in range(5):
                    if (x, y) in p:
                        str_piece += couleur + "■ " + colors.reset
                    else:
                        str_piece += "  "
                # On complète chaque bloc pour qu'il fasse exactement LARGEUR_BLOC
                ligne_formes += str_piece + "  " 
            lignes_finales.append(ligne_formes)
            
        lignes_finales.append("") # Espace entre les rangées

    return lignes_finales

def afficher_jeu_complet(grille, joueur):
    visuel_droite = generer_visuel_pieces(joueur)
    lignes_grille = []
    hauteur_grille = len(grille)
    largeur_grille = len(grille[0])

    # 1. Entête des colonnes (ex: 1  2  3  ...)
    # Chaque numéro occupe 3 espaces via f"{col:<3}"
    entete = "    " + "".join([f"{col:<3}" for col in range(1, largeur_grille + 1)])
    lignes_grille.append(entete)

    # 2. Construction des lignes de la grille
    for i in range(hauteur_grille):
        # Numéro de ligne (2 chiffres) + 2 espaces
        ligne_txt = f"{i + 1:>2}  "
        for j in range(largeur_grille):
            cellule = grille[i][j]
            if cellule == '_':
                # Une case vide prend 1 caractère + 2 espaces = 3
                ligne_txt += "_  "
            else:
                # Un pion (■) prend 1 caractère + 2 espaces = 3
                # Les codes couleurs ne comptent pas dans la largeur visuelle
                ligne_txt += f"{cellule}  " 
        lignes_grille.append(ligne_txt)

    # 3. Affichage avec zone gauche fixe
    # On définit une largeur fixe pour que le séparateur '|' ne bouge pas
    # 16 colonnes * 3 espaces + marge gauche = environ 55-60
    LARGEUR_COLONNE_GAUCHE = 55 

    print("\n" + "=" * 120)

    nb_lignes = max(len(lignes_grille), len(visuel_droite))
    for i in range(nb_lignes):
        gauche = lignes_grille[i] if i < len(lignes_grille) else ""
        
        # On calcule la longueur réelle sans les codes ANSI pour le padding
        visible = gauche.replace(colors.reset, "").replace('\033', '').replace('[31m', '').replace('[34m', '').replace('■', 'X')
        padding = " " * (LARGEUR_COLONNE_GAUCHE - len(visible))
        
        separateur = " | "
        droite = visuel_droite[i] if i < len(visuel_droite) else ""
        
        print(f"{gauche}{padding}{separateur}{droite}")


# pour compter les scores
def calculer_score(joueur):
    """
    Règles :
    - Chaque carré restant en main = -1 point.
    - Si toutes les pièces sont posées = +15 points.
    - Si la dernière pièce posée est le monomino (et toutes posées) = +20 points.
    """
    if not joueur.pieces:
        # Le joueur a tout posé
        if getattr(joueur, 'derniere_piece_etait_un_par_un', False):
            return 20
        return 15

    # Sinon, on compte les carrés restants en négatif
    malus = 0
    for p in joueur.pieces:
        malus -= len(p)
    return malus

# Vérifie si la pièce est le carré 1x1
def est_monomino(piece):
    return len(piece) == 1
