import os
import string
import nltk
import sys
import numpy
from operator import itemgetter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r') as f:
            files[f] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    """words = [word.lower() for word in nltk.word_tokenize(document)]
    filtered = words.copy()
    for word in words:
        if word in string.punctuation:
            filtered.remove(word)
        if word in nltk.corpus.stopwords.words("english"):
            filtered.remove(word)"""
    words = [word.lower() for word in nltk.word_tokenize(document) if not (word in string.punctuation or word in
                                                                           nltk.corpus.stopwords.words("english"))]
    # Watch out for and& or statements etc. --> break down into simple pieces using parentheses
    # Refactoring: Write code that serves the exact same purpose as before but is improved in terms of implementation

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    values = []
    for words in documents.values():
        for word in words:
            values.append(word)

    total_docs = len(documents)

    for word in values:
        containing_words = 0
        for values in documents.values():
            if word in values:
                containing_words += 1

        idfs[word] = numpy.log(total_docs / containing_words)

    return idfs


def counter(sentence, element):
    num = 0
    for word in sentence:
        if word == element:
            num += 1

    return num


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = {file: 0 for file in files}
    for word in query:
        for file, words in files.items():
            frequency = counter(words, word)
            if frequency != 0:
                tf_idf[file] += frequency * idfs[word]

    sorted_tf_idf = sorted([file for file in files], key=lambda x: tf_idf[x], reverse=True)

    return sorted_tf_idf[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top = []
    for sentence, sentence_words in sentences.items():
        sentence_idf = 0
        for word in query:
            if word in sentence_words:
                sentence_idf += idfs[word]
        top.append([sentence, sentence_idf])

    sorted_top = sorted(top, key=itemgetter(1), reverse=True)

    sorted_sentences = [sentence[0] for sentence in sorted_top[:n]]

    return sorted_sentences


if __name__ == "__main__":
    main()
