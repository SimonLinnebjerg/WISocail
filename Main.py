from FileHandler import FileHandler
import numpy as NM
file_object = open("C:/Users/Simon/Desktop/Friendships.txt", "r")

filefyr = FileHandler(file_object)
listOfPersons = filefyr.readPersons()

Dmatrix = NM.zeros((listOfPersons.__len__(), listOfPersons.__len__()))
Amatrix = NM.zeros((listOfPersons.__len__(), listOfPersons.__len__()))
counter = 0
for i in listOfPersons:
    Dmatrix[counter][counter] = i.friends.__len__()
    counter2 = 0

    for j in listOfPersons:

        if j.name in i.friends:
            Amatrix[counter][counter2] = 1
        counter2 += 1
    counter += 1

count1=1
count3=1
for i in listOfPersons:
    count3 = 1
    for j in listOfPersons:
        if Amatrix[count1-1][count3-1] == 1:
            print Amatrix[count1 -1][count3 -1]
        count3 += 1
        if count3 == 4218:
            break

    count1 += 1
    if count1 == 4218:
        break







