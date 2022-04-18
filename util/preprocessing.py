from part1 import *
import xml.etree.ElementTree as ET
import math

Tree1 = ET.parse("treeA.xml")
Tree2 = ET.parse ("treeB.xml")
Tree3 = ET.parse("treeC.xml")
Tree4 =  ET.parse("treeD.xml")
Tree5 = ET.parse("treeE.xml")
Tree6 = ET.parse("treeF.xml")
ignoredWords = ["a", "also", "because", "an", "and","are" , "as" , "at" , "from" , "for" , "however" ,"is","an" ,"located" ,"founded" , "it", "is" , "in"]

def organizeDocument(*args):
    documentList = []
    i = 0
    for a in args:
        documentList.append(getTF(a))
        i = i+1
    print(documentList)

    for entry in documentList:
        copyofDict = dict(entry)
        for key in copyofDict:
            if(key in ignoredWords):
                entry.pop(key)
    print(documentList)
    return documentList

def getTFIDF (vectorList):
    termcounter = 0

    for entry in vectorList:
        for key in entry:
            for i in range(len(vectorList)):
                if (key in vectorList[i]):
                    termcounter += 1
            DF = float(len(vectorList) / termcounter)
            value = math.log10(DF)
            entry[key] = entry.get(key)*value
            termcounter = 0


    return vectorList



def containsText(node):
    flag = False
    if (node.text is None):
        flag = False
    elif (node.text.isspace()):
        flag = False
    else:
        flag = True
    return flag



def getAllText(doc):
    stringMatrix = {}
    for node in doc.iter():
        if(node.text is not node):
            tokenizedtext = node.text.split()
            for word in tokenizedtext:
                if(word not in stringMatrix):
                     stringMatrix[word] = 0
    return stringMatrix


def getStructureTF(doc):
    matrixRep = {}
    stringRep = getAllText(doc)
    matrixtoAdd = {}
    root = doc.getroot()
    iteration = 0
    path = ""
    for node in doc.iter():
        path += "" + node.tag + "/"
        if(containsText(node)):
            tokenizedText = node.text.split()
            for word in stringRep:
                if(word in tokenizedText):
                    matrixtoAdd[word] = 1
                else:
                    matrixtoAdd[word] = 0

            iteration+=1
            dict2 = matrixtoAdd.copy()
            matrixRep[path]= dict2
            path = ""+str(root.tag)+"/"
    return matrixRep






def getALlTFStruct(*args):
    fullMatrixList = []
    for a in args:
        fullMatrixList.append(getStructureTF(a))
    return fullMatrixList

def getIDFStruct (matrixList):
    termCounter = 0
    for entry in matrixList:
        for key in entry:
            for i in range(len(matrixList)):
                if(key in matrixList[i]):
                    dict1 = entry.get(key)
                    dict2 = matrixList[i].get(key)
                    for child in dict1:
                        if(child in dict2 and dict2.get(child) != 0 ):
                            termCounter+=1


def getMatrixLength(matrix):
    total = 0
    for entry in matrix:
        dict1 = matrix.get(entry)
        values = dict1.values()
        for value in values:
            total+= value**2
    return total

def getCosineSimMatrix(matrix1,matrix2):
    numerator = 0
    lengthMatrix1 = getMatrixLength(matrix1)
    lengthMatrix2 =  getMatrixLength(matrix2)
    for entry in matrix1:
        dict1 = matrix1.get(entry)
        dict2 = matrix2.get(entry)
        if(entry in matrix2):
            for child in dict1:
                if(child in dict2):
                    numerator+= dict1.get(child)*dict2.get(child)
    denom = float(math.sqrt(lengthMatrix1 * lengthMatrix2))
    cosSim = numerator/denom

    return cosSim




























#print(getTFIDF(organizeDocument(Tree1,Tree2,Tree3,Tree4)))
vectorList = getALlTFStruct(Tree5,Tree6)
print(getCosineSimMatrix(vectorList[0],vectorList[1]))












