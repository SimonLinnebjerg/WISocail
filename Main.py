from FileHandler import FileHandler
import numpy as NM
file_object = open("C:/Users/Simon/Desktop/friendshipstest.txt", "r")

filefyr = FileHandler(file_object)
listOfPersons = filefyr.readPersons()

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




print loweigenvalue
print loweigenvector

count = 0
for i in loweigenvector:
    listOfPersons[count].eigenvectorvalue = i

#sortedpersonlist = sorted(listOfPersons, key=)

listOfPersons.sort(key=lambda x: x.eigenvectorvalue)

print listOfPersons[0].eigenvectorvalue
print listOfPersons[1].eigenvectorvalue





