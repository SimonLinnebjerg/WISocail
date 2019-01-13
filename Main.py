from FileHandler import FileHandler
import CommunityDetection
import SentimentAnalysis
from tensorflow import keras
import numpy as np
import Person
import random

file_object = open("C:/Users/mathias/Desktop/friendships.reviews.txt", "r")
train_object = open("C:/Users/mathias/Desktop/sentimenttrainingdata.txt", "r")
test_object = open("C:/Users/mathias/Desktop/sentimenttestingdata.txt", "r")

file_handler = FileHandler()
training_person_list = file_handler.read_test_or_training(train_object)
test_person_list = file_handler.read_test_or_training(test_object)
listOfPersons = file_handler.readPersons(file_object)


for i in training_person_list:
    i.review = SentimentAnalysis.negate(i.review)
    i.summary = SentimentAnalysis.negate(i.summary)

for i in listOfPersons:
    i.review = SentimentAnalysis.negate(i.review)
    i.summary = SentimentAnalysis.negate(i.summary)

for i in test_person_list:
    i.review = SentimentAnalysis.negate(i.review)
    i.summary = SentimentAnalysis.negate(i.summary)

vocab_size, allthewords = SentimentAnalysis.create_dictionary(training_person_list, test_person_list, listOfPersons)

community1, community2 = CommunityDetection.CommunityDetection(listOfPersons)


def get_community(person):
    if person in community1:
        return community1
    else:
        return community2


def person_likes_fine_food(person: Person):
    score = 0
    counter = 0
    for i in person.friends:
        for j in listOfPersons:
            if i == j.name:
                if j.score != 0:
                    if (j.score < 1):
                        print(j.name, j.score)
                    if j in get_community(person):
                        if j.name == "kyle":
                            score += j.score * 10
                            counter += 10
                        else:
                            score += j.score
                    else:
                        if j.name == "kyle":
                            score += j.score * 100
                            counter += 100
                        else:
                            score += j.score * 10
                            counter += 10
    return score / (len(person.friends) + counter)


def who_are_likely():
    resultlist = []
    for i in listOfPersons:
        if len(i.summary) == 0:
            i.score = person_likes_fine_food(i)
            if (i.score > 3):
                resultlist.append(str(i.name) + " " + str(i.score) + " - Will buy: Yes" + "\n")
            else:
                resultlist.append(str(i.name) + " " + str(i.score) + " - Will buy: No" + "\n")
    return resultlist



def give_reviewers_scores(all_persons):
    model = SentimentAnalysis.load_model()

    u=0
    k=1
    featureList = []
    temp = []

    for i in all_persons:
        temp = []
        if len(i.review) != 0:
            for j in i.summary:
                temp.append(allthewords[j])
            for j in i.review:
                temp.append(allthewords[j])
            featureList.append(temp)

    featureList = keras.preprocessing.sequence.pad_sequences(featureList, value=allthewords["<PAD>"], padding='post', maxlen=256)
    print(featureList)

    for i in all_persons:
        if len(i.review) != 0:
            tempresult = model.predict(featureList[u:k])
            max = np.argmax(tempresult)
            i.score = tempresult                     #np.argmax(model.predict(featureList[u:k])) + 1
            u += 1
            k += 1

'''   
temppersons = []
for i in all_persons:
    if len(i.review) != 0:
        temppersons.append(SentimentAnalysis.to_nn_input_format(i, allthewords))
                
predicted_scores = np.argmax(model.predict(temppersons))   #random.randint(1, 5)
'''



give_reviewers_scores(listOfPersons)
result = who_are_likely()
print(result)

