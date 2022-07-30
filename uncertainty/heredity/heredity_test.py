import unittest
import heredity


class TestHeredity(unittest.TestCase):
    def setUp(self):
        self.people = {
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }

        self.one_gene = {"Harry"}
        self.two_genes = {"James"}
        self.has_trait = {"James"}
        self.probabilities = {
            "Harry": {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0
                },
                "trait": {
                    True: 0,
                    False: 0
                }
            },
            "James": {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0
                },
                "trait": {
                    True: 0,
                    False: 0
                }
            },
            "Lily": {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0
                },
                "trait": {
                    True: 0,
                    False: 0
                }
            }
        }

    def test_inheritance_probability_no_gene(self):
        probs = heredity.inheritance_probability(0)
        self.assertEqual(probs, 0.01)

    def test_inheritance_probability_one_gene(self):
        probs = heredity.inheritance_probability(1)
        self.assertEqual(probs, 0.5)

    def test_inheritance_probability_two_genes(self):
        probs = heredity.inheritance_probability(2)
        self.assertEqual(probs, 0.99)

    def test_parent_gene_count(self):
        parent_genes = heredity.parent_gene_count(self.people, self.one_gene, self.two_genes, child="Harry")
        self.assertEqual(parent_genes, {"mother": 0, "father": 2})

    def test_grouper_Harry(self):
        group = heredity.grouper("Harry", self.one_gene, self.two_genes, self.has_trait)
        self.assertEqual(group, {"gene_count": 1, "trait": False})

    def test_grouper_Lily(self):
        group = heredity.grouper("Lily", self.one_gene, self.two_genes, self.has_trait)
        self.assertEqual(group, {"gene_count": 0, "trait": False})

    def test_grouper_James(self):
        group = heredity.grouper("James", self.one_gene, self.two_genes, self.has_trait)
        self.assertEqual(group, {"gene_count": 2, "trait": True})

    def test_joint_probability(self):
        joint_probability = heredity.joint_probability(self.people, self.one_gene, self.two_genes, self.has_trait)
        self.assertEqual(joint_probability, 0.0026643247488)

    def test_update(self):
        heredity.update(self.probabilities, self.one_gene, self.two_genes, self.has_trait, 0.0026643247488)
        updated_probabilities = self.probabilities = {
            "Harry": {
                "gene": {
                    2: 0,
                    1: 0.0026643247488,
                    0: 0
                },
                "trait": {
                    True: 0,
                    False: 0.0026643247488
                }
            },
            "James": {
                "gene": {
                    2: 0.0026643247488,
                    1: 0,
                    0: 0
                },
                "trait": {
                    True: 0.0026643247488,
                    False: 0
                }
            },
            "Lily": {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0.0026643247488
                },
                "trait": {
                    True: 0,
                    False: 0.0026643247488
                }
            }
        }

        self.assertEqual(updated_probabilities, self.probabilities)


