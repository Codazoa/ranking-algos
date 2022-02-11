import getopt, sys
from os.path import exists
import math
import csv

class TF_IDF(object):
    """ docstring """
    def __init__(self, dataFile):
        self.termIndex = {}
        pass

    def rankQuery(self, Q, k):
        self.tf_idf(Q, k)

    def tf_idf(self, Q, k):
        print(f'Using TF_IDF on {Q} {k}')
        pass

    def relevance(self, d, Q):
        pass

    def tf(self, d, t):
        return math.log(1 + (__docFreq(d, t)/__numTerms(d)))

    def __docFreq(self, d, t):
        pass

    def __numTerms(self, d):
        pass


class BM_25(object):
    """ docstring """
    def __init__(self, dataFile):
        pass

    def rankQuery(self, Q, k):
        self.bm25(Q, k)

    def bm25(self, Q, k):
        print(f'Using BM_25 on {Q} {k}')
        pass


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
        query = input('\nEnter query to search:\t(--exit to exit) \n')
        if(query == '--exit'): # exit input and program
            return
        results = input('Enter number of results to show? \n')
        print()

        # make sure results is actually a number
        if(not results.isnumeric()):
            print('Enter a valid number')
            continue

        # calcualte rank for the query
        print(rank.rankQuery(query, results))






    pass

if __name__ == '__main__':
    main()
