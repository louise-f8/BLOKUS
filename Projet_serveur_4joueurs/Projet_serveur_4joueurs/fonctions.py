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
        print(f"{col:<3}", end="")
    print()
    for i in range(hauteur):
        print(f"{i + 1:>2}  ", end="")
        for j in range(largeur):
            print(f"{grille[i][j]}  ", end="")
        print()

# Rotation 90° horaire
def rotation_90(piece):
    p = [(y, -x) for (x, y) in piece]
    min_x = min(x for x, y in p)
    min_y = min(y for x, y in p)
    return [(x - min_x, y - min_y) for (x, y) in p]

# Miroir horizontal
def rotation_miroir(piece):
    p = [(-x, y) for (x, y) in piece]
    min_x = min(x for x, y in p)
    min_y = min(y for x, y in p)
    return [(x - min_x, y - min_y) for (x, y) in p]

# liste de toutes les orientations possible de la pièce
def toutes_orientations(piece):
    orientations = []
    p = piece
    for _ in range(4):
        p_triee = sorted(p)
        if p_triee not in orientations: orientations.append(p_triee)
        p = rotation_90(p)
    p = rotation_miroir(piece)
    for _ in range(4):
        p_triee = sorted(p)
        if p_triee not in orientations: orientations.append(p_triee)
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
        os.system('cls' if os.name == 'nt' else 'clear')
        afficher_jeu_complet(grille, joueur)
        print(f"\nC'est au tour du joueur {joueur.color.upper()}")
        choix = input(f"Choisissez une pièce ({choix_possibles[0]}-{choix_possibles[-1]}) : ").upper().strip()
        if choix in choix_possibles:
            index = int(choix[1:]) - 1
            return joueur.pieces[index], choix
        input("Choix invalide ! Entrée pour réessayer.")


def supprimer_piece(joueur, nom_piece):
    index = int(nom_piece[1:]) - 1
    joueur.pieces.pop(index)

def placement_valide(coords, grille, joueur, est_premier, coins_dispo):
    touche_coin = False
    contact_diag = False
    c_joueur = getattr(colors.fg, joueur.color) + '■' + colors.reset

    for x, y in coords:
        if not (0 <= x < len(grille[0]) and 0 <= y < len(grille)): return False
        if grille[y][x] != '_': return False

        if est_premier:
            if (x, y) in coins_dispo: touche_coin = True
        else:
            adj = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
            for ax, ay in adj:
                if 0 <= ax < len(grille[0]) and 0 <= ay < len(grille):
                    if grille[ay][ax] == c_joueur: return False
            diag = [(x-1,y-1), (x-1,y+1), (x+1,y-1), (x+1,y+1)]
            for dx, dy in diag:
                if 0 <= dx < len(grille[0]) and 0 <= dy < len(grille):
                    if grille[dy][dx] == c_joueur: contact_diag = True
    return touche_coin if est_premier else contact_diag


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


def afficher_grille_interactive(grille, piece, position, joueur):
    temp_grille = copy.deepcopy(grille)
    px0, py0 = position
    for dx, dy in piece:
        x, y = px0 + dx, py0 + dy
        if 0 <= x < len(temp_grille[0]) and 0 <= y < len(temp_grille):
            temp_grille[y][x] = getattr(colors.fg, joueur.color) + '■' + colors.reset
    os.system('cls' if os.name == 'nt' else 'clear')
    afficher_jeu_complet(temp_grille, joueur) # Utilisation de la vue complète ici aussi

def placement_interactif(grille, rotations, joueur, est_premier, coins_dispo):
    idx, pos = 0, [0, 0]
    while True:
        piece = rotations[idx]
        afficher_grille_interactive(grille, piece, pos, joueur)
        print(f"\nPosition: {pos[0]+1},{pos[1]+1} | Espace: Tourner | Entrée: Valider | 'q': Retour")
        key = readchar.readkey()
        if key.lower() == 'q': return "CHANGER"
        if key.lower() == 'p': return "BLOQUER"
        if key == readchar.key.UP: pos[1] = max(0, pos[1]-1)
        elif key == readchar.key.DOWN: pos[1] = min(len(grille)-1, pos[1]+1)
        elif key == readchar.key.LEFT: pos[0] = max(0, pos[0]-1)
        elif key == readchar.key.RIGHT: pos[0] = min(len(grille[0])-1, pos[0]+1)
        elif key == readchar.key.SPACE: idx = (idx + 1) % len(rotations)
        elif key == readchar.key.ENTER:
            coords = [(pos[0]+dx, pos[1]+dy) for dx, dy in piece]
            if placement_valide(coords, grille, joueur, est_premier, coins_dispo): return coords
            print("Placement invalide !"); time.sleep(1)

def formater_grille_couleurs(grille_brute):
    """Transforme les mots 'red'/'blue' en carrés colorés pour l'affichage"""
    nouvelle_grille = [ligne[:] for ligne in grille_brute]
    for y in range(len(nouvelle_grille)):
        for x in range(len(nouvelle_grille[0])):
            if nouvelle_grille[y][x] == 'red':
                nouvelle_grille[y][x] = colors.fg.red + '■' + colors.reset
            elif nouvelle_grille[y][x] == 'blue':
                nouvelle_grille[y][x] = colors.fg.blue + '■' + colors.reset
    return nouvelle_grille

def afficher_jeu_complet(grille, joueur):
    visuel_droite = generer_visuel_pieces(joueur)
    lignes_grille = []
    largeur_grille = len(grille[0])

    entete = "    " + "".join([f"{col:<3}" for col in range(1, largeur_grille + 1)])
    lignes_grille.append(entete)

    for i in range(len(grille)):
        ligne_txt = f"{i + 1:>2}  "
        for j in range(largeur_grille):
            cellule = grille[i][j]
            ligne_txt += f"{cellule}  " if cellule != '_' else "_  "
        lignes_grille.append(ligne_txt)

    print("\n" + "=" * 120)
    nb_lignes = max(len(lignes_grille), len(visuel_droite))
    
    for i in range(nb_lignes):
        gauche = lignes_grille[i] if i < len(lignes_grille) else ""
        visible = gauche.replace(colors.reset, "").replace('\033', '').replace('[31m', '').replace('[34m', '').replace('■', 'X')
        padding = " " * (LARGEUR_COLONNE_GAUCHE - len(visible))
        
        separateur = " | "
        droite = visuel_droite[i] if i < len(visuel_droite) else ""
        print(f"{gauche}{padding}{separateur}{droite}")

def generer_visuel_pieces(joueur, pieces_par_ligne=7):
    # Calcul du score : 89 total - carrés restants en main
    score_actuel = 89 - sum(len(p) for p in joueur.pieces)
    
    lignes_finales = [
        f"--- PIÈCES DISPONIBLES ({joueur.color.upper()}) ---",
        f"SCORE ACTUEL : {score_actuel} pts",
        ""
    ]
    couleur = getattr(colors.fg, joueur.color)
    LARGEUR_BLOC = 12 

    for i in range(0, len(joueur.pieces), pieces_par_ligne):
        groupe = joueur.pieces[i: i + pieces_par_ligne]
        
        # Ligne des noms (P1, P2...)
        ligne_noms = ""
        for j in range(len(groupe)):
            nom = f"P{i + j + 1}"
            ligne_noms += f"{nom:<{LARGEUR_BLOC}}"
        lignes_finales.append(ligne_noms)

        # Dessin des formes
        for y in range(5):
            ligne_formes = ""
            for p in groupe:
                str_piece = ""
                for x in range(5):
                    if (x, y) in p:
                        str_piece += couleur + "■ " + colors.reset
                    else:
                        str_piece += "  "
                ligne_formes += str_piece + "  " 
            lignes_finales.append(ligne_formes)
        lignes_finales.append("") 
    return lignes_finales


def calculer_score(joueur):
    return 89 - sum(len(p) for p in joueur.pieces)

def fin_jeu(j1, j2): return not j1.pieces or not j2.pieces
def grille_pleine(g): return all(cell != '_' for row in g for cell in row)
def joueur_suivant(curr, list_j): return list_j[(list_j.index(curr) + 1) % len(list_j)]