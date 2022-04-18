import xml.etree.ElementTree as ET
import math
#load or parse the file

Tree1 = ET.parse("treeA.xml")
Tree2 = ET.parse ("treeB.xml")
Tree3 =  ET.parse("treeC.xml")
Tree4 = ET.parse("treeD.xml")
rootA = Tree1.getroot()
vectorRepresentation  = {}

def getTF (Tree1):
    vectorRepresentation ={}
    for child in Tree1.iter():
        if(child.tag not in vectorRepresentation):
            vectorRepresentation[child.tag] = 1
        else:
            vectorRepresentation[child.tag] = vectorRepresentation.get(child.tag) +1
        if (child.text is not None):
         tokenizedText = child.text.split()
         for word in tokenizedText:
                if(word not in vectorRepresentation):
                    vectorRepresentation[word] = 1
                else:
                    vectorRepresentation[word] = vectorRepresentation.get(word) +1

    return vectorRepresentation


def getVectorRepresentationText(fileName):
    vectorRepresentation = {}
    with open(fileName , 'r') as file:
        for line in file:
            for word in line.split():
                if(word not in vectorRepresentation):
                    vectorRepresentation[word] = 1
                else:
                    vectorRepresentation[word] = vectorRepresentation.get(word)+1

    return vectorRepresentation


def getIndexingNodes(Tree):
    indexingNodes = []
    indexingNodes.append(Tree.getroot().tag)
    for node in Tree.iter():
        if(node.text is None ):
            print("Empty Node is null")
        elif (node.text.isspace()):
            print("Node is Space")
        else:
            indexingNodes.append(node.tag)
    return indexingNodes


def augmentVectors (Vector1 , Vector2):
    for key in Vector1:
        if(key not in Vector2):
            Vector2[key] = 0
    for key2 in Vector2:
        if(key2 not in Vector1):
            Vector1[key2] = 0

def getCosineSimilarity(Vector1, Vector2):
    #augmentVectors(Vector1 , Vector2)
    numerator = 0
    sumVector1 = 0
    sumVector2 = 0

    for key in Vector1:
      numerator +=   Vector1.get(key) * Vector2.get(key)
      sumVector1 += Vector1.get(key)**2
      sumVector2 += Vector2.get(key)**2

    cosineSim = numerator / math.sqrt(sumVector1 * sumVector2)

    return cosineSim















#vectorRepresentation = getTF(Tree1)
#vectorRepresentation2 = getTF(Tree2)
#print(vectorRepresentation2 , vectorRepresentation)
#augmentVectors(vectorRepresentation , vectorRepresentation2)
#print(vectorRepresentation2 , vectorRepresentation)
#print(getCosineSimilarity(vectorRepresentation,vectorRepresentation2))
#print(getIndexingNodes(Tree1))
indexingNodes = getIndexingNodes(Tree1)
#print(vectorRepresentation)
print(indexingNodes)






