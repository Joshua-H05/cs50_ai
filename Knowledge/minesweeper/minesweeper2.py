import itertools
import random
import copy



class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.mines = None
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        self.mines = set()
        if len(self.cells) == self.count:
            for cell in tuple(self.cells):
                self.mines.add(cell)
            return self.mines
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        cells = self.cells
        if self.count == 0:
            return cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def new_sentence(self, cell, count):
        unidentified_neighbors = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if i in range(0, 8) and j in range(0, 8):
                    unidentified_neighbors.add((i, j))

        already_identified = set()
        for neighbor in unidentified_neighbors:
            if neighbor in self.safes:
                already_identified.add(neighbor)

            if neighbor in self.mines:
                already_identified.add(neighbor)
                count -= 1

            if neighbor == cell:
                unidentified_neighbors.remove(neighbor)

        for identified_neighbor in already_identified:
            unidentified_neighbors.remove(identified_neighbor)

        sentence = [unidentified_neighbors, count]
        if sentence not in self.knowledge:
            self.knowledge.append(sentence)

    def additional_labeling(self):
        for sentence in copy.deepcopy(self.knowledge):
            if sentence[1] == 0:
                for cell in sentence[0]:
                    self.safes.add(cell)
                self.knowledge.remove(sentence)

            elif len(sentence[0]) == sentence[1]:
                for cell in sentence[0]:
                    self.mines.add(cell)
                self.knowledge.remove(sentence)

    def subset_inference(self):
        new_sentences = []

        for main_set in self.knowledge:
            for subset in self.knowledge:

                if subset[0] == main_set[0]:
                    continue

                if subset[0].issubset(main_set[0]):
                    new_set = main_set[0] - subset[0]
                    new_set_count = main_set[1] - subset[1]
                    new_sentences.append([new_set, new_set_count])

        for sentence in new_sentences:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)
        new_sentences.clear()

    def cleanup(self):
        known = set()
        for sentence in self.knowledge:
            for cell in sentence[0]:
                if cell in self.safes:
                    known.add(cell)
                if cell in self.mines:
                    known.add(cell)
                    sentence[1] -= 1

            for known_cell in known:
                sentence[0].remove(known_cell)
            known.clear()

    def update_based_on_cell(self, cell):
        for sentence in self.knowledge:
            if cell in copy.deepcopy(sentence[0]):
                sentence[0].remove(cell)

    def cell_sentence(self, cell, count):
        neighbors = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if i in range(0, 8) and j in range(0, 8):
                    if (i, j) != cell:
                        neighbors.add((i, j))

        sentence = [neighbors, count]

        for cell in copy.deepcopy(sentence[0]):
            if cell in self.safes:
                sentence[0].remove(cell)
            if cell in self.mines:
                sentence[0].remove(cell)
                sentence[1] -= 1
        if sentence not in self.knowledge:
            self.knowledge.append(sentence)
        return sentence

    def new_sentences(self, cell, count):
        new_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) != cell:

                    if (i, j) in self.safes:
                        continue

                    if (i, j) in self.mines:
                        count = count - 1
                        continue

                    if 0 <= i < self.height and 0 <= j < self.width:
                        new_cells.add((i, j))
        self.knowledge.append(Sentence(new_cells, count))

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.new_sentences(cell, count)
        self.mark_safe(cell)
        self.moves_made.add(cell)

        additions = True

        while additions:
            additions = False
            safe_cells = set()
            mines = set()

            for sentence in copy.deepcopy(self.knowledge):
                useless = Sentence(set(), 0)
                if sentence == useless:
                    self.knowledge.remove(sentence)

            for sentence in self.knowledge:
                mines = mines.union(sentence.known_mines())
                safe_cells = safe_cells.union(sentence.known_safes())

            if safe_cells:
                additions = True
                for safe in safe_cells:
                    self.mark_safe(safe)

            if mines:
                additions = True
                for mine in mines:
                    self.mark_mine(mine)

            for subset in self.knowledge:
                for main_set in self.knowledge:

                    if subset.cells == main_set.cells:
                        continue

                    if subset.cells.issubset(main_set.cells):
                        cells = main_set.cells - subset.cells
                        count = main_set.count - subset.count

                        new = Sentence(cells, count)

                        if new not in self.knowledge:
                            additions = True
                            self.knowledge.append(new)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = set()
        for move in self.safes:
            if move not in self.moves_made:
                possible_moves.add(move)
        if len(possible_moves) == 0:
            return None
        else:
            move = random.choice(tuple(possible_moves))
            return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        height = 8
        width = 8
        for i in range(height):
            for j in range(width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.add((i, j))
        if len(possible_moves) == 0:
            return None
        else:
            move = random.choice(tuple(possible_moves))
            return move
