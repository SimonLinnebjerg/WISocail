
class Person:
    def __init__(self, name, friends, summary, review):
        if "\n" in name:
            self.name = name.replace("\n", "")
        else:
            self.name = name
        self.friends = friends
        self.summary = summary
        self.review = review
        self.eigenvectorvalue = 0

    def __init__(self, name):
        self.name = name
        self.friends = []
