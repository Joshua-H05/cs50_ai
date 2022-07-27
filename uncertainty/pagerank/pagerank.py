import os
import random
import re
import sys
import pysnooper

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
    links = len(corpus[page])
    linked = []
    for page in corpus[page]:
        linked.append(page)

    if links:
        for page in corpus.keys():
            probability_distribution[page] = round((1 - damping_factor) / len(corpus), 4)

        for page in linked:
            probability_distribution[page] = round(probability_distribution[page] + damping_factor / links, 4)

    else:
        for link in corpus:
            probability_distribution[link] = 1 / len(corpus)

    return probability_distribution


"""@pysnooper.snoop(depth=2)"""


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_probability = dict()
    all_pages = []
    possible_pages = []
    page_probabilities = []

    for page in corpus.keys():
        sample_probability[page] = 0
        all_pages.append(page)

    clicked = random.choice(all_pages)
    sample_probability[page] += 1 / n

    for value in range(1, n):
        transition = transition_model(corpus, clicked, damping_factor)
        for page, probability in transition.items():
            possible_pages.append(page)
            page_probabilities.append(probability)
        clicked = random.choices(possible_pages, page_probabilities)[0]
        sample_probability[clicked] += 1 / n
        possible_pages.clear()
        page_probabilities.clear()

        sample_sum = 0
    for rank in sample_probability.values():
        sample_sum += rank
    print(f" Sample sum: {sample_sum}")
    print(sample_probability)

    return sample_probability


"""@pysnooper.snoop()"""


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    n = len(corpus)
    counter = 0

    for page in corpus.keys():
        pagerank[page] = 1 / n
    while True:
        for page in pagerank.keys():
            sigma = 0
            for key, value in corpus.items():
                if page in value:
                    sigma += pagerank[key] / len(value)
                if len(value) == 0:
                    sigma += pagerank[key] / len(corpus)

            new_pr = (1 - damping_factor) / n + damping_factor * sigma

            if abs(new_pr - pagerank[page]) < 0.0001:
                counter += 1

            pagerank[page] = new_pr

            if counter == n:
                iteration_sum = 0
                for rank in pagerank.values():
                    iteration_sum += rank

                print(f"Iteration sum: {iteration_sum}")
                print(pagerank)
                print(corpus)

                return pagerank
                break


if __name__ == "__main__":
    main()
