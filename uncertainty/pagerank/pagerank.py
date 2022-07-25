import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = dict()
    linked = len(corpus[page])

    if linked:
        for link in corpus[page]:
            probability_distribution[link] = damping_factor / len(linked)
            probability_distribution[link] += (1 - damping_factor) / len(corpus)

    else:
        for link in corpus:
            probability_distribution[link] = 1 / len(corpus)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_probability = {}
    all_pages = []

    for page in corpus.keys():
        sample_probability[page] = 0
        all_pages.append(page)

    page = random.choice(all_pages)
    sample_probability[page] += 1/n

    page_transition_model = transition_model(corpus, page, damping_factor)
    possible_pages = []
    page_probabilities = []

    for key, value in page_transition_model.items():
        possible_pages.append(key)
        page_probabilities.append(value)

    for value in range(1, n):
        clicked = random.choices(possible_pages, page_probabilities)
        sample_probability[clicked] += 1/n
        possible_pages.clear()
        page_probabilities.clear()

        chosen_transition_model = transition_model(corpus, clicked, damping_factor)
        for page, probability in chosen_transition_model.items():
            possible_pages.append(page)
            possible_pages.append(probability)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    """pagerank = dict()
    n = len(corpus)
    all_pages = []
    converged = 0
    previous_paper_rank = None
    linking_pages = dict()

    for page in corpus.keys():
        pagerank[page] = 1/n
        all_pages.append(page)

    while True:
        for page in all_pages:
            previous_paper_rank = pagerank[page]
            pagerank[page] = (1 - damping_factor) / n
            for key, value in corpus.items():
                if page in value:"""
    pass





if __name__ == "__main__":
    main()
