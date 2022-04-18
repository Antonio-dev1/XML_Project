from preprocessing import *
import math

def getEuclideanDistance (vector1 , vector2):
    sumofVectors = 0
    for key in vector1:
        if key not in vector2:
            sumofVectors += vector1.get(key)**2
        else:
            sumofVectors += math.pow(vector1.get(key) - vector2.get(key), 2)
    distance = math.sqrt(sumofVectors)
    return distance


def querytoVector(query):
    stringList = query.split(" ")
    queryVector = {}
    for word in stringList:
        if word in ignoredWords:
            continue
        elif word not in queryVector:
            queryVector[word] = 1
        else:
            queryVector[word] = queryVector[word] + 1
    return queryVector


def getKNN(documentVectors , query , K):
    distanceDictionary = {}
    documentList = []
    queryVector = querytoVector(query)
    countingIndex = 0
    documentLabelIndex  = 1
    for doc in documentVectors:
        distanceDictionary['query/' + 'Doc' + str(documentLabelIndex)] = getEuclideanDistance(doc, queryVector)
        documentLabelIndex+=1
    print(distanceDictionary)
    sortedDict = sorted(distanceDictionary , key = distanceDictionary.get)
    print(sortedDict)
    for key in sortedDict:
        if(countingIndex == K):
            break
        else:
            documentList.append(key)
        countingIndex+=1
    return documentList




documentList = getTFIDF(organizeDocument(Tree1,Tree2,Tree3,Tree4))
finalList = getKNN(documentList , "Beirut" , 2)
print(finalList)













