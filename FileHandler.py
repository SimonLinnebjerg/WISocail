from Person import Person, Testreview


class FileHandler:

    def remove_value_from_list(self, list, val):
        return [value for value in list if value != val]

    def read_test_or_training(self, testfileortrainingfile):
        file = testfileortrainingfile
        testList = []
        fileData = file.readlines()
        count = 0
        varSumm = []
        varscore = 0
        varReview = []
        for f in fileData:
            if "review/score:" in f:
                number = f.split(" ")[1]
                number = number.replace("\n", "")
                varscore = float(number)
            if "review/summary:" in f:
                varSumm = self.stringCleaner(f)
                varSumm = varSumm.split(" ")[2:]
                if "*" not in f:
                    self.remove_value_from_list(varSumm, '\n')
                    for i in varSumm:
                        if "\n" in i:
                            varSumm[len(varSumm) - 1] = i.replace("\n", "")
                    varSumm = self.remove_value_from_list(varSumm, '')
            if "review/text:" in f:
                varReview = self.stringCleaner(f)

                varReview = varReview.split(" ")[2:]
                if "*" not in f:
                    for i in varReview:
                        if "\n" in i:
                            varReview[len(varReview) - 1] = i.replace("\n", "")
                    varReview = self.remove_value_from_list(varReview, "")
                count += 1
                testList.append(Testreview(varSumm, varReview, varscore))
        return testList


    def readPersons(self, personfile):
        personList = []
        fileData = personfile.readlines()
        count = 0
        for f in fileData:
            if "user:" in f:
                self.remove_value_from_list(f, '\n')
                namevar = f.split(" ")[1]
                if "\n" in namevar:
                    namevar = namevar.split("\n")[0]
                personList.append(Person(namevar))
            if "friends:" in f:
                varList = f.split("\t")[1:]
                for i in varList:
                    if "\n" in i:
                        varList[len(varList) -1] = i.replace("\n", "")
                varList = self.remove_value_from_list(varList, '')
                personList[count].friends.extend(varList)
            if "summary:" in f:
                varSumm = self.stringCleaner(f)
                varSumm = varSumm.split(" ")[2:]
                if "*" not in f:
                    for i in varSumm:
                        if "\n" in i:
                            varSumm[len(varSumm) -1] = i.replace("\n", "")
                    varSumm = self.remove_value_from_list(varSumm, '')
                    personList[count].summary.extend(varSumm)
            if "review:" in f:
                varReview = self.stringCleaner(f)
                varReview = varReview.split(" ")[2:]
                if "*" not in f:
                    for i in varReview:
                        if "\n" in i:
                            varReview[len(varReview) -1] = i.replace("\n", "")
                    varReview = self.remove_value_from_list(varReview, '')
                    personList[count].review.extend(varReview)
                count += 1
        return personList

    def stringCleaner(self, input):
        input = input.lower()
        cleansed = input.replace(".", " . ")
        cleansed = cleansed.replace("!", " ! ")
        cleansed = cleansed.replace("?", " ? ")
        cleansed = cleansed.replace(";", " ; ")
        cleansed = cleansed.replace(":", " : ")
        cleansed = cleansed.replace("  ", " ")


        return cleansed
