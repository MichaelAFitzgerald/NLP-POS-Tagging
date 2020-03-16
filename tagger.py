# Michael Fitzgerald
# 2/28/2020

# 1 explanation of the program
# This program will take in two files, the training data and the testing data
# The tagger program will run some pre-processing steps to remove non-relevant tokens like brackets
# The program then splits the word/tag combos by whitespace and then breaks them down into discrete words and tags
# After that, we use the training data to look at all the words and their associated tags
# tracking the frequencies and using them to create a model that would calculate the probability
# of a tag belonging to any given word
# We then do that exact thing on the test data, creating a list of word/tag combos
# on the test data before we output the list to the scorer program to be graded

# 2 example input/output of the program
# Given training data: "Hello/NN Goodbye/DT"
# and test data: "Hello Goodbye"
# This program should output: "Hello/NN|DT Goodbye/NN|DT"

# 3 breakdown of the program
# Read the pos-train.txt and pos-test.txt files
# convert them to strings
# the strings are then converted into lists to be used in the remainder of the program
# the specific lists being wordList: a list of all unique words in the training data
# tagList: a list of all unique tags in the training data
# tagOrder: a list of all tags in the training data in the order they appeared, including duplicates
# using the tagList, we create a dictionary containing the frequencies for all single tags in the training data
# and using the tagList and wordList we create a new dictionary
# that will contain the frequencies of all possible word/tag combinations
# then finally we create another dictionary using tagOrder to count the frequencies
# for all possible combinations of previous tags and current tags
# now that we have all the necessary frequencies we can use the helper functions defined below to calcuate
# the probability of a tag belonging to a given word, and use the test data to do so
# once the tagger program is done, we save the data in a new text file and pass it along to the scorer

import re
import io
import scorer


# begin function definitions

# Parameters:
# currentTag - the string containing the current tag
# currentWord - the string containing the current word
# prevTag - the string containing the previous tag
# singleTagDict - the dictionary containing the frequencies of all the tags,
# to be passed as a parameter to other functions
# wordTagDict - the dictionary containing the frequencies of certain word/tag combos
# to be passed as a parameter to the other functions
# tagComboDict - the dictionary containing the frequencies for prevTag/Tag combos
# to be passed as a parameter to the other functions
# Explanation:
# The function will call calcWordProb and calcTagProb
# and return their product
def getTotalProb(currentTag, currentWord, prevTag, singleTagDict, wordTagDict, tagComboDict):
    wordProb = calcWordProb(currentWord, currentTag, singleTagDict, wordTagDict)
    tagProb = calcTagProb(currentTag, prevTag, singleTagDict, tagComboDict)
    return wordProb * tagProb


# Parameters:
# currentTag - the string containing the current tag
# currentWord - the string containing the current word
# singleTagDict - the dictionary containing the frequencies of all the tags,
# to be passed as a parameter to other functions
# wordTagDict - the dictionary containing the frequencies of certain word/tag combos
# to be passed as a parameter to the other functions
# Explanation:
# calls getSingleTagFreq into tagFreq and the frequency of the currentWord/currentTag
# via the wordTagDict into wordTagFreq
# returns wordTagFreq / tagFreq
def calcWordProb(currentWord, currentTag, singleTagDict, wordTagDict):
    tagFreq = getSingleTagFreq(currentTag, singleTagDict)
    wordDict = wordTagDict.get(currentTag)
    if wordDict is None:
        wordTagFreq = 0
    else:
        wordTagFreq = wordDict.get(currentWord)
        if wordTagFreq is None:
            wordTagFreq = 0
    return wordTagFreq / tagFreq


# Parameters:
# currentTag - the string containing the current tag
# currentWord - the string containing the current word
# singleTagDict - the dictionary containing the frequencies of all the tags,
# to be passed as a parameter to other functions
# tagComboDict - the dictionary containing the frequencies for prevTag/Tag combos
# to be passed as a parameter to the other functions
# Explanation:
# calls getSingleTagFreq into prevTagFreq and gets the tagComboFreq from
# the tagComboDict via the prevTag and currentTag
# returns tagComboFreq / prevTagFreq
def calcTagProb(currentTag, prevTag, singleTagDict, tagComboDict):
    prevTagFreq = getSingleTagFreq(prevTag, singleTagDict)
    if prevTagFreq is None:
        prevTagFreq = 1
    newComboDict = tagComboDict.get(prevTag)
    if newComboDict is None:
        tagComboFreq = 0
    else:
        tagComboFreq = tagComboDict.get(prevTag).get(currentTag)
    return tagComboFreq / prevTagFreq


# Parameters:
# tag - the string containing the current tag
# tagDict - the dictionary containing the frequencies of all the tags
# Explanation:
# queries the tagDict for the frequency of the given tag
# returns the count
def getSingleTagFreq(tag, tagDict):
    tagCount = tagDict.get(tag)
    return tagCount


# Parameters:
# prevTag - the previous tag in the tagList
# tag - the current tag in the tagList
# tagList - the tags in order of appearance in the corpus
# Explanation:
# given the prevTag and tag, will iterate through the tagList
# counting the number of times prevTag -> tag appears
# and returns that count
def countTagCombos(prevTag, tag, tagList):
    count = 0

    for i in range(len(tagList)):
        if i == 0:
            continue
        if tagList[i] == tag:
            if tagList[i - 1] == prevTag:
                count += 1
    return count


# begin main execution
def main():
    # import the necessary files
    testFile = io.open("Provided/pos-test.txt")
    trainFile = io.open("Provided/pos-train.txt")

    # get the actual txt from the files
    testData = testFile.read()
    trainData = trainFile.read()

    # remove '[', ']' characters from the training and testing data
    trainData = re.sub('[\[|\]]', '', trainData)
    testData = re.sub('[\[|\]]', '', testData)

    # create a list of all the word/tag combos
    wordTagList = re.split('\s+', trainData)
    wordTagList.remove('')

    # create three dictionaries
    # tagList - the list of all unique tags in the corpus
    # tagOrder - the list of all the tags from the corpus in order
    # wordList - the list of all unique words in the corpus
    tagList = []
    tagOrder = []
    wordList = []

    # iterate through wordTagList and separate the word from the tag
    for wordTag in wordTagList:
        currentPair = re.split('/', wordTag)
        # if there is no word/tag pair
        if len(currentPair) is 1:
            continue
        # if there was an additional backslash that split the word
        elif len(currentPair) > 2:
            first = re.sub("\\\\", '', currentPair[0])
            newWord = first + '/' + currentPair[1]
            currentPair[0] = newWord
            currentPair[1] = currentPair[2]

        # add to the respective lists
        if currentPair[0] not in wordList:
            wordList.append(currentPair[0])
        if currentPair[1] not in tagList:
            tagList.append(currentPair[1])
        tagOrder.append(currentPair[1])

    # initialize a dictionary for tag frequencies
    tagFreq = dict()

    # get the frequencies for every tag
    for tag in tagList:
        count = trainData.count(tag)
        tagFreq.update({tag: count})

    # get the frequencies of every word/tag pairing
    wordTagFreq = dict()
    for tag in tagList:
        wordTagDict = dict()
        for word in wordList:
            wordTagPair = word + '/' + tag
            wordTagCount = trainData.count(wordTagPair)
            wordTagDict.update({word: wordTagCount})
        wordTagFreq.update({tag: wordTagDict})

    # get the frequencies for the tag | prevTag combos
    tagComboFreq = dict()
    for prevTag in tagList:
        newTagFreq = dict()
        for tag in tagList:
            comboCount = countTagCombos(prevTag, tag, tagOrder)
            newTagFreq.update({tag: comboCount})
        tagComboFreq.update({prevTag: newTagFreq})

    # now run the test file
    # get all the words from the testData
    testList = re.split('\s+', testData)

    # create the wordTags collection for the testData so it can be outputted
    testWordTags = []
    prevTag = '<s>'

    # for each word in testList
    for word in testList:
        # calculate the probability of that word belonging to a tag
        bestProb = -1.0
        bestTag = ''
        for tag in tagList:
            tagProb = getTotalProb(tag, word, prevTag, tagFreq, wordTagFreq, tagComboFreq)
            # if the tagProb is higher than the current value of bestProb
            # replace bestProb and bestTag
            if tagProb > bestProb:
                bestProb = tagProb
                bestTag = tag
        # set the prevTag to the tag that was just used
        prevTag = bestTag
        testWordTags.append({'Word': word, 'Tag': bestTag})

    # call the scorer program to evaluate the tagger
    # needs to be changed to use STDOUT ??
    print(testWordTags)

    # create and write to a file object with our testGuesses
    saveFile = open('Provided/pos-testGuess.txt', 'w')
    saveFile.write(str(testWordTags))

    scorer.scorer(testWordTags, None)

    scorer.sendToScorer('Provided/pos-testGuess.txt', 'Provided/pos-test-key.txt')


# calls the main function
if __name__ == '__main__':
    main()

# end of program
