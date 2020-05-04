from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
            Or(AKnight,AKnave),                             #Chevalier ou valet
            Implication(AKnight,And(AKnight,AKnave)),        #Si chevalier-> (AChevalier et AValet)
            Implication(AKnave,Not(And(AKnight,AKnave)))     #Si Valet -> Not(AChevalier et AValet)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
            Or(AKnight,AKnave),                             #A Chevalier ou valet
            Or(BKnight,BKnave),                             #B Chevalier ou valet
            Implication(AKnight,And(AKnave,BKnave)),        #Si AChevalier -> (AKnave et BKnave)
            Implication(AKnave,Not(And(AKnave,BKnave)))      #Si BChevalier -> Not(AValet et BValet)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
            Or(AKnight,AKnave),                            #A Chevalier ou valet
            Or(BKnight,BKnave),                            #B Chevalier ou valet
            Implication(AKnight,Or(And(AKnight,BKnight),And(AKnave,BKnave))),  #A chevalier -> (Achevalier et BChevalier) ou (AValet et BValet)
            Implication(BKnight,Or(And(AKnight,BKnave),And(AKnave,BKnight))),
            Implication(AKnave,Not(Or(And(AKnight,BKnight),And(AKnave,BKnave)))),  #A chevalier -> (Achevalier et BChevalier) ou (AValet et BValet)
            Implication(BKnave,Not(Or(And(AKnight,BKnave),And(AKnave,BKnight))))   #B chevalier -> (BChevalier et AValet) OU (BValet et Achevalier)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight,AKnave),                            #A Chevalier ou valet
    Or(BKnight,BKnave),                            #B Chevalier ou valet
    Or(CKnight,CKnave),                            #C Chevalier ou valet
    Implication(BKnight,And(AKnave,CKnave)),       #B chevalier -> AValet et CValet
    Implication(BKnave,Not(And(AKnave,CKnave))),   #B Valet -> Not (AValet et CValet)
    Implication(CKnight,AKnight),       #B chevalier -> AValet et CValet
    Implication(CKnave,AKnave),
    Implication(AKnight,Or(AKnight,AKnave)),
    Implication(AKnave,Not(Or(AKnight,AKnave)))
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
