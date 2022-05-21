import math
from preprocessing import *
from postProcessing import*
documentID = ["Doc 1" ,"Doc 2", "Doc 3" ,"Doc 4","Doc 5","Doc 6","Doc 7","Doc 8","Doc 9","Doc 10" ,
              "Doc 11","Doc 12","Doc 13","Doc 14","Doc 15","Doc 16","Doc 17","Doc 18","Doc 19","Doc 20",
              "Doc 21","Doc 22","Doc 23","Doc 24","Doc 25","Doc 26","Doc 27","Doc 28","Doc 29","Doc 30",
              "Doc 31","Doc 32","Doc 33","Doc 34","Doc 35","Doc 36","Doc 37","Doc 38","Doc 39","Doc 40",
              "Doc 41","Doc 42","Doc 43", "Doc 44"]
queryTree = ET.parse("query.xml")


def getIndexingStructure(vectorList):
    termcounter = 0
    id = ""
    indexingStructure ={}

    for entry in vectorList:
        for key in entry:
            if(key not in indexingStructure):
                for i in range(len(vectorList)):
                    if (key in vectorList[i]):
                        termcounter += 1
                        id+=documentID[i]+","
                DF = float(len(vectorList) / termcounter)
                value = math.log10(DF)
                indexingStructure[key] = id+str(value)
                id=""
                termcounter = 0

    return indexingStructure


def getIndexing(query, indexingStructure , listofVectors):
    SimValues ={}
    documentsGoneOver = []
    queryVector = querytoVector(query)
    copy_indexingStructure = indexingStructure.copy()
    for entry in queryVector.copy():
        if entry in indexingStructure:
            keyList = copy_indexingStructure.get(entry).split(",")
            keyList.pop()
            for key in keyList:
               print(key.isnumeric())
               if(key not in documentsGoneOver and  not key.isnumeric()):
                documentsGoneOver.append(key)
                temp = key.split(" ")
                SimValues[key] = getCosineSimilarity(listofVectors[int(temp[1]) -1] , queryVector)

    return SimValues


def getResultFromIndexing(SimValues , k):
    sortedDict = sorted(SimValues, key=SimValues.get, reverse=True)
    documentList = []
    countingIndex = 0
    if k > len(SimValues):
        k = len(SimValues)

    for key in sortedDict:
        if (countingIndex == k):
            break
        else:
            documentList.append(str(key).replace(" ",""))
        countingIndex += 1
    return documentList


def getIndexingTableStruct(fileNames):
    table = {}
    for file in fileNames:
        doc = ET.parse(file)
        root = doc.getroot()
        for node in doc.iter():
            if node.text is not None:
                string = node.text.split()
                if string:
                    currentNode = node
                    currentPath = node.tag
                    while currentNode !=root:
                        currentNode = doc.find(f'.//{currentNode.tag}/..')
                        currentPath = currentNode.tag + "/" + currentPath
                    for word in string:
                        path = currentPath + f'/{word}'
                        if path not in table:
                            table[path] = []
                        table[path].append(file)
    N=len(fileNames)
    for el in table:
        table[el].append(math.log10((N)/len(table[el])))
    return table



def filterDocuments(query , structIndexTable):
    queryTree = ET.parse(query)
    queryMatrix = getStructureTF(queryTree)
    relevantDocuments = []
    queryKey = ""
    for key in structIndexTable:
        pathList = str(key).split("/")
        finalWord  = pathList.pop()
        for path in pathList:
            queryKey = queryKey+ path+"/"
        if(queryKey in queryMatrix):
            dict1 = queryMatrix.get(queryKey)
            if(finalWord in dict1):
                if(dict1.get(finalWord)!=0):
                    documents = structIndexTable.get(key)
                    documents.pop()
                    for doc in documents:
                        if(doc not in relevantDocuments):
                            relevantDocuments.append(doc)
        queryKey =""
    return relevantDocuments

def getSimFromStruct(query , K, filteredDocs,matrixList):
    Tree = ET.parse(query)
    docsIDS = []
    simKeys = {}
    documentstoReturn = []
    countingIndex = 0
    queryMatrix = getStructureTF(Tree)
    for doc in filteredDocs:
        if(doc in corpus):
            docsIDS.append(corpus.get(doc)-1)

    for id in docsIDS:
        simKeys["Doc"+str(id+1)] = getCosineSimMatrix(queryMatrix ,matrixList[id])
    sortedDictionary = sorted(simKeys , key = simKeys.get , reverse = True)
    if(len(filteredDocs) < K):
        K = len(filteredDocs)

    for key in sortedDictionary:
        if (countingIndex == K):
            break
        else:
            documentstoReturn.append(str(key).replace(" ", ""))
        countingIndex += 1
    return documentstoReturn





Tfvector = organizeDocument(parsedTrees(documents))
idfvectorList = getDFFlatText(Tfvector)
print( getIndexingStructure(Tfvector))

#tfIDFVector = getTFIDF(Tfvector)
#Values = getIndexing("Paris", IndexStructure , idfvectorList)
#listofDocs = getResultFromIndexing(Values , 3)
#print(Values)
#print(listofDocs)
#print(getResultFromIndexing(simValues , 3))
#print(getResultFromIndexing(simValues , 1))
structIndex = getIndexingTableStruct(documents)
print(structIndex)
#print(structIndex)

vectorList = getALlTFStruct(parsedTrees(documents))
IDFvector = getIDFStruct(vectorList)
#print(IDFvector)
#print(getSimFromStruct("query.xml" , 3,filteredDocuments , IDFvector))
filteredDocuments = filterDocuments("query.xml",structIndex )
print(filteredDocuments)
lsitofSim = getSimFromStruct("query.xml" , 3 , filteredDocuments , IDFvector)
print(lsitofSim)
print(matchIDtoDocs(lsitofSim))
