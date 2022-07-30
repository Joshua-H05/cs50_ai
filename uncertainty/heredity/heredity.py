import csv
import itertools
import sys

import numpy

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
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
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def inheritance_probability(parent_genes):
    inheritance_prob = None
    if parent_genes == 2:
        inheritance_prob = 1 - PROBS["mutation"]
    if parent_genes == 1:
        inheritance_prob = 0.5
    if parent_genes == 0:
        inheritance_prob = PROBS["mutation"]
    return inheritance_prob


def parent_gene_count(people, one_gene, two_genes, child):
    mother = people[child]["mother"]
    father = people[child]["father"]
    mother_genes = 0
    father_genes = 0
    if mother in one_gene:
        mother_genes = 1
    elif mother in two_genes:
        mother_genes = 2

    if father in one_gene:
        father_genes = 1
    elif father in two_genes:
        father_genes = 2

    parent_genes = {"mother": mother_genes, "father": father_genes}
    return parent_genes


def grouper(person, one_gene, two_genes, have_trait):
    gene_count = 0
    if person in one_gene:
        gene_count = 1
    elif person in two_genes:
        gene_count = 2

    trait = None
    if person in have_trait:
        trait = True
    else:
        trait = False

    return {"gene_count": gene_count, "trait": trait}


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_prob = 0
    probs_people = []
    for person in people.keys():
        probability_gene = None
        probability_trait = None

        gene_count = grouper(person, one_gene, two_genes, have_trait)["gene_count"]
        trait = grouper(person, one_gene, two_genes, have_trait)["trait"]

        if people[person]["mother"] is None and people[person]["father"] is None:
            probability_gene = PROBS["gene"][gene_count]

        else:
            mother_genes = parent_gene_count(people, one_gene, two_genes, person)["mother"]
            father_genes = parent_gene_count(people, one_gene, two_genes, person)["father"]

            if gene_count == 0:
                probability_gene = (1 - inheritance_probability(mother_genes)) * \
                                   (1 - inheritance_probability(father_genes))

            if gene_count == 1:
                probability_gene = \
                    inheritance_probability(mother_genes) * (1 - inheritance_probability(father_genes)) + \
                    inheritance_probability(father_genes) * (1 - inheritance_probability(mother_genes))

            if gene_count == 2:
                probability_gene = inheritance_probability(mother_genes) * inheritance_probability(father_genes)

            # Probability of someone having or not having a trait given a number of genes
        probability_trait = PROBS["trait"][gene_count][trait]

        # Probability of someone having a number of genes and either having or not having a trait

        joint = probability_gene * probability_trait
        probs_people.append(joint)

    joint_prob = numpy.prod(probs_people)
    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        num_genes = 0
        if person in two_genes:
            num_genes = 2
        if person in one_gene:
            num_genes = 1
        probabilities[person]["gene"][num_genes] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        crude_probs_gene = 0
        for probs in probabilities[person]["gene"].values():
            crude_probs_gene += probs

        gene_factor = 1 / crude_probs_gene
        for genes, probs in probabilities[person]["gene"].items():
            probabilities[person]["gene"][genes] = probs * gene_factor

        crude_probs_trait = 0
        for probs in probabilities[person]["trait"].values():
            crude_probs_trait += probs

        trait_factor = 1 / crude_probs_trait
        for trait, probs in probabilities[person]["trait"].items():
            probabilities[person]["trait"][trait] = probs * trait_factor


if __name__ == "__main__":
    main()
