import numpy as np





def CommunityDetection(listOfPersons):
    Laplacian = [0] * listOfPersons.__len__()

    count1 = 0
    for i in listOfPersons:
        count = 0
        relationVector = [0] * listOfPersons.__len__()
        for j in listOfPersons:
            for k in i.friends:
                if k == j.name:
                    relationVector[count] = -1

            if count == count1:
                relationVector[count] = i.friends.__len__()
            count += 1
        Laplacian[count1] = relationVector
        count1 += 1

    eigenvalue, eigenvector = np.linalg.eig(Laplacian)

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
        count += 1

    return listOfPersons[0:gapstart + 1], listOfPersons[gapstart + 1:]



