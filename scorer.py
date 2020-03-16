# Michael Fitzgerald
# 2/28/2020

# 1 explanation of the program
# This program will take in either files or lists containing the
# output from tagger.py as well as the pos-test-key.txt
# scorer.py will then iterate through both lists and check how accurate
# the tagger output is compared to the test key

# 2 example input/output of the program
# given the tagger.py output [{Word: Hello, Tag: NN}, {Word: Goodbye, Tag: DT}]
# and the test-key [{Word: Hello, Tag: DT}, {Word: Goodbye, Tag: DT}]
# the scorer.py method would output:
# Given word: Hello, Key word: Hello
# Given tag: NN, Key tag: DT
# Given word: Goodbye, Key word: Goodbye
# Given tag: DT, Key tag: DT
# Total correct: 1
# Total given: 2
# Overall accuracy: 50%

# 3 breakdown of the program
# If called from the commandLine: this program will convert the Files into the format expected by scorer
# Otherwise the scorer method will receive a list and a io.wrapper from the origin
# The test-key is then processed in the same manner as the tagOutput was in the tagger program
# so that the layouts of the collections will be identical
# i.e. removing brackets, splitting the text file into list of words by whitespace
# further splitting the word/tag items by the '/' character
# from there we initialize variables to count the total number of items and the items we correctly labelled
# After each comparison, we print out whether the word or tag matched the test-key
# and after all have been compared show the number correctly guessed, total number, and the overall accuracy


# start of the scorer program
import io
import re
import sys
import ast


def sendToScorer(tagFile, testFile):
    # read the test key
    if testFile is None:
        testKey = io.open("Provided/pos-test-key.txt")
    else:
        testKey = io.open(testFile)

    testGuess = io.open(tagFile)
    tagOutput = ast.literal_eval(testGuess.read())

    scorer(tagOutput, testKey)


def scorer(tagOutput, testKey):
    if testKey is None:
        testKey = io.open("Provided/pos-test-key.txt")

    testKeyData = testKey.read()

    # clean the data
    testKeyData = re.sub('[\[|\]]', '', testKeyData)
    testKeyData = re.sub('\n+', ' ', testKeyData)

    # create a wordTag list from the testKeyData
    keyList = re.split('\s+', testKeyData)
    keyList.remove('')

    # data structure to hold the correct word key pairs
    keyComp = []

    # iterate through the keyList and separate the words from the tags
    for wordTag in keyList:
        currentPair = re.split('/', wordTag)
        if len(currentPair) is 1:
            continue
        elif len(currentPair) > 2:
            first = re.sub("\\\\", '', currentPair[0])
            word = first + '/' + currentPair[1]
            tag = currentPair[2]
        else:
            word = currentPair[0]
            tag = currentPair[1]
        keyComp.append({'Word': word, 'Tag': tag})

    # initialize the variables to count the number of lines gone through
    # and the ones that were correctly tagged
    countTotal = 0
    countCorrect = 0

    for i in range(len(keyComp)):
        # initialize the vars
        countTotal += 1
        compBool = False

        # get the word/tag from the testKey
        keyWord = keyComp[i].get('Word')
        keyTag = keyComp[i].get('Tag')

        # get the word/tag from the tagger
        compWord = tagOutput[i].get('Word')
        compTag = tagOutput[i].get('Tag')

        # if the tagger was correct
        # increment countCorrect and set compBool to true
        if keyTag == compTag:
            countCorrect += 1
            compBool = True
        # print word/tag results to console
        print('Given word: ' + compWord + ' Key word: ' + keyWord)
        print('Given tag: ' + compTag + ' Key tag: ' + keyTag)
        print('Comparison status: ' + str(compBool))
        print('***********************************************************')

    # print final results to console
    print('Total correct: ' + str(countCorrect))
    print('Total given ' + str(countTotal))

    print('Overall accuracy: ' + str((countCorrect / countTotal) * 100) + '%')

    print('End of scorer')


if __name__ == '__scorer__':
    pred = sys.argv[1]
    key = sys.argv[2]

    sendToScorer(pred, key)

# end of program
