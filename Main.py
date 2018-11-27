from FileHandler import FileHandler
from tensorflow import keras
import numpy as NM
import Person
file_object = open("C:/Users/marku/Desktop/friendships.reviews.txt", "r")
train_object = open("C:/Users/marku/Desktop/sentimenttrainingdata.txt", "r")
test_object = open("C:/Users/marku/Desktop/sentimenttestingdata.txt", "r")

#file_object = open("C:/Users/marku/Desktop/friendshipstest.txt", "r")
#train_object = open("C:/Users/marku/Desktop/sentimenttrainingsmall.txt", "r")
#test_object = open("C:/Users/marku/Desktop/sentimenttestingsmall.txt", "r")

filefyr = FileHandler()
training_person_list = filefyr.read_test_or_training(train_object)
test_person_list = filefyr.read_test_or_training(test_object)
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

for  i in training_person_list:
    i.review = negate(i.review)
    i.summary = negate(i.summary)

for i in listOfPersons:
    i.review = negate(i.review)
    i.summary = negate(i.summary)

for i in test_person_list:
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

allthewords["<PAD>"] = 0
allthewords["<START>"] = 1
allthewords["<UNK>"] = 2  # unknown
allthewords["<UNUSED>"] = 3
idx = 4
for i in training_person_list:
    for j in i.summary:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1
    for j in i.review:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1

for i in test_person_list:
    for j in i.summary:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1
    for j in i.review:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1

for i in listOfPersons:
    for j in i.summary:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1
    for j in i.review:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1
'''
train_data = []
test_data = []
markus= []

for i in training_person_list:
    temp_list = []
    for j in i.summary:
        temp_list.append(allthewords[j])
    for j in i.review:
        temp_list.append(allthewords[j])
    train_data.append(temp_list)

for i in test_person_list:
    temp_list = []
    for j in i.summary:
        temp_list.append(allthewords[j])
    for j in i.review:
        temp_list.append(allthewords[j])
    test_data.append(temp_list)

for i in listOfPersons:
    temp_list = []
    for j in i.summary:
        temp_list.append(allthewords[j])
    for j in i.review:
        temp_list.append(allthewords[j])
    markus.append(temp_list)

train_labels = []
for i in training_person_list:
    train_labels.append(i.score)

test_labels = []
for i in test_person_list:
    test_labels.append(i.score)

train_data = NM.array(keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value= allthewords["<PAD>"],
                                                        padding='post',
                                                        maxlen=235))

test_data = NM.array(keras.preprocessing.sequence.pad_sequences(test_data,
                                                       value=allthewords["<PAD>"],
                                                       padding='post',
                                                       maxlen=235))
'''
vocab_size = len(allthewords)
'''
def train_model():
    model = keras.Sequential()
#    model.add(keras.layers.Embedding(vocab_size, 16))
#    model.add(keras.layers.GlobalAveragePooling1D())
#    model.add(keras.layers.Dense(16, activation=TF.nn.relu))
#    model.add(keras.layers.Dense(1, activation=TF.nn.sigmoid))


    model.add(keras.layers.Dense(16, input_shape=(235)))
    model.add(keras.layers.Dense(30, activaction=TF.nn.relu))
    model.add(keras.layers.Dense(1, activation=TF.nn.softmax))

    model.compile(optimizer=TF.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])


    model.fit(train_data,
        train_labels,
        epochs=1,
        batch_size=512,
     #   validation_data=(test_data, test_labels),
        verbose=1)

    model.save("sentimentModel.h5")

'''

def load_model():
    return keras.models.load_model("sentimentModel.h5")




#train_model()
model=load_model()

#print(model.predict(train_data[0]))

def to_nn_input_format(person):
    temp_list = []
    for j in person.summary:
        temp_list.append(allthewords[j])
    for j in person.review:
        temp_list.append(allthewords[j])
    while len(temp_list) < 235:
        temp_list.append("<PAD>")
    return temp_list


def give_reviewers_scores(all_persons):
    for i in all_persons:
        if len(i.review) != 0:
            i.score = model.predict(to_nn_input_format(i))


def get_community(person):
    if person in community1:
        return community1
    else:
        return community2


def person_likes_fine_food(person: Person):
    score = 0
    for i in person.friends:
        for j in listOfPersons:
            if i == j.name:
                if i in get_community(person):
                    if j.name == "kyle":
                        score += j.score * 10
                    else:
                        score += j.score
                else:
                    if j.name == "kyle":
                        score += j.score * 100
                    else:
                        score += j.score * 10
    return score / len(person.friends)


def who_are_likely():
    resultlist = []
    for i in listOfPersons:
        if len(i.summary) == 0:
            i.score = person_likes_fine_food(i)
            resultlist.append(str(i.name) + " " + str(i.score) + "\n")
    return resultlist


result = who_are_likely()
print(result)
