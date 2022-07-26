import unittest
import pagerank


class PageRankTest(unittest.TestCase):
    def setUp(self):
        self.corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"1.html", "2.html", "4.html"},
                       "4.html": {"1.html"}}
        self.damping_factor = 0.85

    def test_transition_model_one_link(self):
        probability_distribution = pagerank.transition_model(self.corpus, "2.html", self.damping_factor)
        self.assertEqual(probability_distribution, {"1.html": 0.0375, "2.html": 0.0375,
                                                    "3.html": 0.8875, "4.html": 0.0375})

    def test_transition_model_two_links(self):
        probability_distribution = pagerank.transition_model(self.corpus, "1.html", self.damping_factor)
        self.assertEqual(probability_distribution, {"1.html": 0.0375, "2.html": 0.4625,
                                                    "3.html": 0.4625, "4.html": 0.0375})

    def test_transition_model_three_links(self):
        probability_distribution = pagerank.transition_model(self.corpus, "3.html", self.damping_factor)
        self.assertEqual(probability_distribution, {"1.html": 0.3208, "2.html": 0.3208,
                                                    "3.html": 0.0375, "4.html": 0.3208})





