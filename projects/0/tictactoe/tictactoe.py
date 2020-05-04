"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY,EMPTY ,EMPTY ],
            [EMPTY, EMPTY,EMPTY ]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #Variable pour compter les X
    nb_coup_X = 0
    #Variable pour compter les 0
    nb_coup_O = 0
    #Parcours les lignes du jeux
    #Compte les coups de chaques joueurs
    for ligne in range(len(board)):
        for colonne in range(len(board[ligne])):
            if board[ligne][colonne] == "X":
                nb_coup_X += 1
            elif board[ligne][colonne] == "O":
                nb_coup_O += 1
    #Etat initial (x commence)
    if nb_coup_O == 0 and nb_coup_X == 0:
        return "X"
    #Tour de X (plus de coup pour O)
    elif nb_coup_X <= nb_coup_O:
        return "X"
    #Tour de O (plus de coup pour X)
    elif nb_coup_X > nb_coup_O:
        return "O"
    #
    else:
        return "O"

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    coups_possibles = set()
    #Parcours les ligne
    #Ajoute au set toutes les colonnes vident
    for ligne in range(len(board)):
        for colonne in range(len(board[ligne])):
            if board[ligne][colonne] == None:
                coups_possibles.add((ligne,colonne))

    return coups_possibles

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #print("Result Board initial",board)
    #Copie la grille
    board_result = copy.deepcopy(board)
    #recupere le joeur qui jouer
    joueur = player(board_result)
    #Modifie la grille
    board_result[action[0]][action[1]] = joueur
    #retourne la grille modifié
    #print("Result board sortie", board)
    return board_result

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    victoire = None
    #Test les lignes
    for i in range(3):
        #Test les lignes
        #Pour pas renvoyer les lignes vides
        if board[i][0] != None:
            if board[i][0] == board[i][1] == board[i][2]:
                victoire = board[i][0]
                return victoire
        #Test les colonnes
        if board[0][i] != None:
            if board[0][i] == board[1][i] == board[2][i]:
                victoire = board[0][i]
                return victoire

    #Test des diagonales
    if board[0][0] != None:
        if board[0][0] == board[1][1] == board[2][2]:
            victoire = board[0][0]
            return victoire
    if board[0][2] != None:
        if board[0][2] == board[1][1] == board[2][0]:
            victoire = board[0][2]
            return victoire

    return victoire
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    resultat = winner(board)
    #Test grille incomplete
    #Si pas de vainqueur et None dans la grille (partie en cours)
    if resultat == None:
        for element in board:
            if None in element:
                return False

    return True


    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    resultat = winner(board)

    if resultat == "X":
        return 1
    elif resultat == "O":
        return -1
    else:
        return 0

    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -2
    for action in actions(board):
        #print(f"max_value action testé {action}")
        #print(f"résultat de la fonction {result(board,action)}")
        v = max(v,min_value(result(board,action)))
        #print(f"max_value Valeur optenue {v}")
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 3
    for action in actions(board):
        #print(f"min_value action testé {action}")
        #print(f"résultat de la fonction {result(board,action)}")
        v = min(v,max_value(result(board,action)))
        #print(print(f"max_value Valeur optenue {v}"))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #Test si la board est terminé
    if terminal(board):
        return None

    current_player=player(board)
    print(f"Joueur qui {current_player} doit jouer")

    liste_actions = actions(board)
    print(f"Coups possible {liste_actions} ")

    score = None
    best_action = None
    i=0
    # IA est le joueur X
    if current_player == "X":
        for element in liste_actions:
            #print(f"Element testé {i}")
            #print(f"Action testée {element}\n")
            t_score = min_value(result(board,element))
            print(f"IA X Action: {element} score: {t_score}")
            #print(f"Valeur max obtenue {t_score}")
            #Initialise le score
            if score == None:
                score = t_score
                best_action = element
            #Selctionne le score le plus haut
            elif t_score > score:
                score = t_score
                best_action = element

            #Si score max retourne la valeur
            """
            if score == 1:
                return best_action
            """
        """
        if score == 1:
            print(f"Meilleur coup possible {best_action}")
            return best_action
        """
    #IA est le joueur O
    else:
        for element in liste_actions:
            #print(f"Element testé {i}")
            print(f"Action testée {element}\n")
            t_score = max_value(result(board,element))
            print(f"IA O Action: {element} score {t_score}")
            #Initialise le score
            if score == None:
                score = t_score
                best_action = element
            #Selectionne la valeur la plus basse
            elif t_score < score:
                score = t_score
                best_action = element

        #Retourne la valeur si minimun
        """
        if score == -1:
            print(f"Meilleur coup possible {best_action}")
            return best_action
        """
    return best_action

    raise NotImplementedError
