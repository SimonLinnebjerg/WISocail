from FileHandler import FileHandler
import tensorflow as TF
from tensorflow import keras
import numpy as NM
file_object = open("C:/Users/Simon/Desktop/friendshipstest.txt", "r")
test_object = open("C:/Users/Simon/Desktop/sentimenttrainingsmall.txt", "r")
filefyr = FileHandler()
testfyr = filefyr.read_test_or_training(test_object)
listOfPersons = filefyr.readPersons(file_object)



def negate(list):
    negatelist = ["never","no","nothing","nowhere","not","havent","hasnt","hadnt","cant","couldnt","shouldnt","wont","wouldnt","dont","dosnt","didnt","isnt","arent","aint"]
    stoplist = [".", ":", ";", "!", "?"]
    negatebool = False
    resultList = []
    for i in list:
        word = i
        if i in negatelist:
            negatebool = not negatebool
            resultList.append(i)
            continue
        if i in stoplist:
            negatebool = False
        if negatebool:
            word = i + "_NEG"
        resultList.append(word)
    return resultList

for  i in testfyr:
    i.review = negate(i.review)
    i.summary = negate(i.summary)

for i in listOfPersons:
    i.review = negate(i.review)
    i.summary = negate(i.summary)


Laplacian = [0] * listOfPersons.__len__()

count1 = 0
for i in listOfPersons:
    count = 0
    relationVector = [0]*listOfPersons.__len__()
    for j in listOfPersons:
        for k in i.friends:
            if k == j.name:
                relationVector[count] = -1

        if count == count1:
            relationVector[count] = i.friends.__len__()
        count += 1
    Laplacian[count1] = relationVector
    count1 += 1

eigenvalue, eigenvector = NM.linalg.eig(Laplacian)

index = eigenvalue.argsort()[::1]

eigenvalue = eigenvalue[index]
eigenvector = eigenvector[:, index]

low = 0
idx = 1
count = 0


for i in eigenvalue[1:]:
    if i == 0:
        idx += 1
    else:
        break

loweigenvalue = eigenvalue[idx]
loweigenvector = eigenvector[idx]

count = 0
for i in loweigenvector:
    listOfPersons[count].eigenvectorvalue = i
    count += 1

listOfPersons.sort(key=lambda x: x.eigenvectorvalue)

largestGap = 0
gapstart = 0
count = 0
for i in listOfPersons:
    if count + 1 == listOfPersons.__len__():
        break
    x = abs(listOfPersons[count + 1].eigenvectorvalue - listOfPersons[count].eigenvectorvalue)
    if largestGap < x:
        largestGap = x
        gapstart = count


community1 = listOfPersons[0:gapstart+1]
community2 = listOfPersons[gapstart+1:]

allthewords = {}
idx = 0
for i in testfyr:
    for j in i.summary:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1
    for j in i.review:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1

print("hey")