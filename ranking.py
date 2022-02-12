import getopt, sys
from os.path import exists
import math
import csv
from functools import reduce

class TF_IDF(object):
    """ docstring """
    def __init__(self, dataFile):
        self.fp = open(dataFile, 'r') # open the csv file
        self.csvData = csv.reader(self.fp) # create a csv reader object
        self.termFreq = {} # calculating term frequencies {'id': [('term', num)]}
        self.docTerms = {} # number of terms in each document {'id': num}
        self.termIndex = {} # inverted index connecting terms to documents {'term': ['id', 'id']}

        for row in self.csvData:
            docId = row[0] # store the docID of current row
            terms = row[1].split() # split the words to count and convert later

            self.termFreq[docId] = [] # initialize this document's list

            self.docTerms[docId] = len(terms) # calculate number of terms in each document
            termSet = set(terms) # convert to set to count individual words
            for term in termSet: # count occurances of each distinct word
                # check if we have this term in the index and add the docID
                if(term not in self.termIndex): self.termIndex[term] = [docId]
                else: self.termIndex[term].append(docId)

                self.termFreq[docId].append((term, row[1].count(term))) # append a new tuple to document's list

        self.fp.close()

    def __getDocsForQuery(self, query): # return list of docId's that correspond to each word in query
        docList = [] # list to hold the docID's
        for term in set(query.split()): # step though each term in the query
            docList = docList + (self.termIndex.get(term)[:])
        return sorted(set(docList)) # cast to set to get distinct values then sort back to a list

    def tf_idf(self, Q, k):
        relList = [] # list of relevance tuples we will return
        docIDList = self.__getDocsForQuery(Q) # get a list of all documents that contain the query terms

        for doc in docIDList:
            relList.append((doc, self.relevance(doc, Q)))

        relList.sort(reverse=True, key=self.__sortRels)

        return relList[:k]

    def relevance(self, d, Q):
        terms = Q.lower().split() # convert words to lower case single words
        if(len(terms) == 1):
            return self.tf(d, Q) / self.__numDocs(Q)

        rel = map( lambda x: self.tf(d, x) / self.__numDocs(x), terms)
        return (reduce( lambda x, y: x + y, rel))

    def tf(self, d, t):
        return math.log(1 + (self.__docFreq(d, t)/self.__numTerms(d)))

    def __docFreq(self, d, t):
        # return number of times term t occurs in document d
        termList = self.termFreq.get(d)
        for tuple in termList:
            if tuple[0] == t:
                return tuple[1]
        return 0

    def __numTerms(self, d):
        # return number of terms in the document
        return self.docTerms.get(d)

    def __numDocs(self, t):
        # return number of documents containing t
        return len(self.termIndex[t])

    def __sortRels(self, tup):
        return tup[1]

    def rankQuery(self, Q, k):
        list = self.tf_idf(Q, k)
        return list

class BM_25(object):
    """ docstring """
    def __init__(self, dataFile):
        self.kVal1 = 1.2
        self.kVal2 = 500
        self.bVal = 0.75

        self.fp = open(dataFile, 'r') # open the csv file
        self.csvData = csv.reader(self.fp) # create a csv reader object
        self.termFreq = {} # calculating term frequencies {'id': [('term', num)]}
        self.docTerms = {} # number of terms in each document {'id': num}
        self.termIndex = {} # inverted index connecting terms to documents {'term': ['id', 'id']}

        for row in self.csvData:
            docId = row[0] # store the docID of current row
            terms = row[1].split() # split the words to count and convert later

            self.termFreq[docId] = [] # initialize this document's list

            self.docTerms[docId] = len(terms) # calculate number of terms in each document
            termSet = set(terms) # convert to set to count individual words
            for term in termSet: # count occurances of each distinct word
                # check if we have this term in the index and add the docID
                if(term not in self.termIndex): self.termIndex[term] = [docId]
                else: self.termIndex[term].append(docId)

                self.termFreq[docId].append((term, row[1].count(term))) # append a new tuple to document's list

        self.fp.close()

    def bm25(self, query, k):
        print(f'Using BM_25 on {Q} {k}')
        terms = query.lower().split() # split up the terms and convert to lower case
        pass

    def __numOfDocs(self):
        # return number of documents in corpus



    def rankQuery(self, Q, k):
        list = self.bm25(Q, k)
        return list

def main(argv = sys.argv[1:]):

    # argument error checking
    if(len(argv) < 2): # not enough arguments
        print('Error: Please provide a ranking algorithm and filename')
        print('Ex: python3 ranking.py [-algorithm] [filename]')
        print('TF_IDF:\t-t  --tfidf')
        print('BM_25:\t-b  --bm25')
        return
    elif(len(argv) > 2): # too many arguments
        print('Error: Wrong number of arguments')
        print('Ex: python3 ranking.py [-algorithm] [filename]')
        return
    elif(not exists(argv[1])): # file exists check
        print(f'Error: <{argv[1]}> does not exist')
        return

    # setting data file to use
    dataFile = argv[1]

    # set up options for changing algorithms
    opts = 'bt'
    fullOpts = ['bm25', 'tfidf']

    # create rank so we can use it later
    rank = ''

    try:
        # get arguments and values
        arg, val = getopt.getopt(argv, opts, fullOpts)
        for curArg, val in arg:
            # use bm25 if user enters this flag
            if curArg in ('-b', '--bm25'):
                print(f'Using BM_25 ranking on {dataFile}')
                rank = BM_25(dataFile)
                break
            # use tfidf if user enters this flag
            elif curArg in ('-t', '--tfidf'):
                print(f'Using TF_IDF ranking on {dataFile}')
                rank = TF_IDF(dataFile)
                break

    # handle the error for unknown options
    except getopt.error as err:
        print(str(err))

    # loop to get input from user
    while True:
        # get query and number of results to show from user
        query = input('\nEnter query to search:\t(--exit to exit)\n-> ')
        if(query == '--exit'): # exit input and program
            return
        results = input('Enter number of results to show?\n-> ')
        print()

        # make sure results is actually a number
        if(not results.isnumeric()):
            print('Enter a valid number')
            continue

        # calcualte rank for the query
        relevance = rank.rankQuery(query, int(results))
        for rel in relevance:
            print(rel)


if __name__ == '__main__':
    main()
