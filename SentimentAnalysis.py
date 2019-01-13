from tensorflow import keras
import numpy as np
import tensorflow as TF

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



def create_dictionary(training_person_list, test_person_list, listOfPersons):
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

    vocab_size = len(allthewords)

    return vocab_size, allthewords


def load_model():
    return keras.models.load_model("sentimentModel.h5")


def to_nn_input_format(person, allthewords):

    temp_list = []
    for j in person.summary:
        temp_list.append(allthewords[j])
    for j in person.review:
        temp_list.append(allthewords[j])
    #while len(temp_list) < 256:
     #   temp_list.append(allthewords["<PAD>"])
    temp_list = keras.preprocessing.sequence.pad_sequences(temp_list,
                                                        value=allthewords["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)

    return temp_list


def train_neural_network(training_person_list, allthewords, test_person_list):
    train_data = []
    test_data = []
    markus = []

    # make train and test feature vectors
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

    # Make labels for train and test data
    train_labels = []
    for i in training_person_list:
        if i.score == 3:
            train_labels.append(2)
        elif i.score == 4:
            train_labels.append(3)
        elif i.score == 5:
            train_labels.append(4)
        elif i.score == 2:
            train_labels.append(1)
        elif i.score == 1:
            train_labels.append(0)

    test_labels = []
    for i in test_person_list:
        if i.score == 3:
            test_labels.append(2)
        elif i.score == 4:
            test_labels.append(3)
        elif i.score == 5:
            test_labels.append(4)
        elif i.score == 2:
            test_labels.append(1)
        elif i.score == 1:
            test_labels.append(0)

    train_labels = np.array(train_labels)
    test_labels = np.array(test_labels)


    train_data = (keras.preprocessing.sequence.pad_sequences(train_data,
                                                             value=allthewords["<PAD>"],
                                                             padding='post',
                                                             maxlen=256))

    test_data = (keras.preprocessing.sequence.pad_sequences(test_data,
                                                            value=allthewords["<PAD>"],
                                                            padding='post',
                                                            maxlen=256))
    vocab_size = len(allthewords)
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=TF.nn.relu))
    model.add(keras.layers.Dense(5, activation=TF.nn.softmax))

    model.compile(optimizer=TF.train.AdamOptimizer(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_data,
              train_labels,
              epochs=3,
              batch_size=512,
              validation_data=(test_data, test_labels),
              verbose=1)

    model.save("sentimentModel.h5")

    e1 = model.evaluate(test_data, test_labels, verbose=2)
    print(e1)
