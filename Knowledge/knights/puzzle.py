from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

general_knowledge = And(
    # Each character is either a knight or a knave but not both
    # A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # C
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
)

statement_0 = And(AKnight, AKnave)
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    general_knowledge,
    Implication(AKnight, statement_0),
    Implication(AKnave, Not(statement_0)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

statement_1a = And(AKnave, BKnave)
knowledge1 = And(
    general_knowledge,
    Implication(AKnight, statement_1a),
    Implication(AKnave, Not(statement_1a))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    general_knowledge,
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
statement_3a = And(Or(AKnight, AKnave),
                   Not(And(AKnight, AKnave)))
knowledge3 = And(
    general_knowledge,
    # A
    Implication(AKnight, statement_3a),
    Implication(AKnave, Not(statement_3a)),
    # B
    Implication(BKnight, And(Not(statement_3a), CKnave)),
    Implication(BKnave, And(statement_3a, CKnight)),
    # C
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),
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
