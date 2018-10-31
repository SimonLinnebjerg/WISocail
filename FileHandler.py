from Person import Person

class FileHandler:

    def __init__(self, filetohandle):
        self.personfile = filetohandle

    def readPersons(self):
        personList = []
        fileData = self.personfile.readlines()
        count = 0
        for f in fileData:
            if "user" in f:
                personList.append(Person(f.split(" ")[1]))
            if "friend" in f:
                varList = f.split("\t")[1:]
                for i in varList:
                    if "\n" in i:
                        varList[len(varList) -1] = i.replace("\n", "")
                personList[count].friends.extend(varList)
                count += 1
        return personList
