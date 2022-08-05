import unittest
import generate
import crossword


class TestCrossWordCreator(unittest.TestCase):
    def setUp(self) -> None:
        self.crossword = crossword.Crossword("data/structure0.txt", "data/words0.txt")
        self.crossword_creator = generate.CrosswordCreator(self.crossword)

    def test_enforce_node_consistency(self):
        self.crossword_creator.enforce_node_consistency()
        for variable, words in self.crossword_creator.domains.items():
            for word in words:
                self.assertEqual(variable.length, len(word))

    def test_revise_no_revision(self):
        result = self.crossword_creator.revise(crossword.Variable(0, 1, 'across', 3),
                                               crossword.Variable(4, 1, 'across', 4))
        self.assertEqual(result, False)

    def test_revise_revision_true(self):
        self.crossword_creator.enforce_node_consistency()
        result = self.crossword_creator.revise(crossword.Variable(0, 1, 'down', 5),
                                               crossword.Variable(4, 1, 'across', 4))
        self.assertEqual(result, True)
        self.assertEqual(self.crossword_creator.domains[crossword.Variable(0, 1, 'down', 5)],
                         {'SEVEN'})
        self.assertEqual(self.crossword_creator.domains[crossword.Variable(4, 1, 'across', 4)],
                         {'FOUR', 'NINE', 'FIVE'})

    def test_ac3_no_given_arc(self):
        self.crossword_creator.enforce_node_consistency()
        result = self.crossword_creator.ac3()
        self.assertEqual(result, True)

    def test_ac3_given_arc(self):
        self.crossword_creator.enforce_node_consistency()
        result = self.crossword_creator.ac3(arcs=[(crossword.Variable(0, 1, 'down', 5),
                                                   crossword.Variable(4, 1, 'across', 4))])
        self.assertEqual(result, True)
        self.assertEqual(self.crossword_creator.domains[crossword.Variable(0, 1, 'down', 5)],
                         {'SEVEN'})
        self.assertEqual(self.crossword_creator.domains[crossword.Variable(4, 1, 'across', 4)],
                         {'FOUR', 'NINE', 'FIVE'})

    # Haven't tested behaviour if no result

    def test_assignment_complete_true(self):
        assignment = {crossword.Variable(4, 1, 'across', 4): "x",
                      crossword.Variable(0, 1, 'down', 5): "y",
                      crossword.Variable(0, 1, 'across', 3): "y",
                      crossword.Variable(1, 4, 'down', 4): "z"}

        result = self.crossword_creator.assignment_complete(assignment)
        self.assertEqual(result, True)

    def test_assignment_complete_false(self):
        assignment = {crossword.Variable(0, 1, 'down', 5): "y",
                      crossword.Variable(0, 1, 'across', 3): "y",
                      crossword.Variable(1, 4, 'down', 4): "z"}

        result = self.crossword_creator.assignment_complete(assignment)
        self.assertEqual(result, False)

    def test_length_true(self):
        result = self.crossword_creator.check_length(crossword.Variable(0, 1, 'down', 5), "eight")
        self.assertEqual(result, True)

    def test_length_false(self):
        result = self.crossword_creator.check_length(crossword.Variable(0, 1, 'down', 5), "nine")
        self.assertEqual(result, False)

    def test_check_uniqueness_true(self):
        assignment = {crossword.Variable(4, 1, 'across', 4): "x",
                      crossword.Variable(0, 1, 'down', 5): "a",
                      crossword.Variable(0, 1, 'across', 3): "y",
                      crossword.Variable(1, 4, 'down', 4): "z"}
        result = self.crossword_creator.check_uniqueness(assignment)
        self.assertEqual(result, True)

    def test_check_uniqueness_false(self):
        self.crossword_creator.enforce_node_consistency()
        assignment = {crossword.Variable(4, 1, 'across', 4): "x",
                      crossword.Variable(0, 1, 'down', 5): "y",
                      crossword.Variable(0, 1, 'across', 3): "y",
                      crossword.Variable(1, 4, 'down', 4): "z"}
        result = self.crossword_creator.check_uniqueness(assignment)
        self.assertEqual(result, False)

    def test_check_arc_consistency_true(self):
        self.crossword_creator.enforce_node_consistency()
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = self.crossword_creator.check_arc_consistency(assignment)
        self.assertEqual(result, True)

    def test_check_node_consistency_true(self):
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = generate.CrosswordCreator.check_node_consistency(self, assignment)
        self.assertEqual(result, True)

    def test_check_node_consistency_false(self):
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVEE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = generate.CrosswordCreator.check_node_consistency(self, assignment)
        self.assertEqual(result, False)

    def test_check_consistent_true(self):
        self.crossword_creator.enforce_node_consistency()
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = self.crossword_creator.consistent(assignment)
        self.assertEqual(result, True)

    def test_check_consistent_false(self):
        self.crossword_creator.enforce_node_consistency()
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NNINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = self.crossword_creator.consistent(assignment)
        self.assertEqual(result, False)

    def test_select_unassigned_variable(self):
        assignment = {
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): "SIX",
                      }
        variable = self.crossword_creator.select_unassigned_variable(assignment)
        self.assertEqual(variable, crossword.Variable(1, 4, 'down', 4))

    def test_backtrack_complete(self):
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = self.crossword_creator.backtrack(assignment)
        self.assertEqual(result, assignment)

    def test_backtrack_incomplete(self):
        self.crossword_creator.enforce_node_consistency()
        assignment = {crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      }
        complete_assignment = {
                      crossword.Variable(1, 4, 'down', 4): 'FIVE',
                      crossword.Variable(0, 1, 'down', 5): 'SEVEN',
                      crossword.Variable(4, 1, 'across', 4): 'NINE',
                      crossword.Variable(0, 1, 'across', 3): 'SIX'}
        result = self.crossword_creator.backtrack(assignment)
        self.assertEqual(assignment, complete_assignment)
