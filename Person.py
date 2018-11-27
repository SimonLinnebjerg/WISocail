
class Person:
    def __init__(self, name):
        if "\n" in name:
            self.name = name.replace("\n", "")
        else:
            self.name = name
        self.friends = []
        self.summary = []
        self.review = []
        self.eigenvectorvalue = 0


class Testreview:
    def __init__(self, summary, review, score):
        self.summary = summary
        self.review = review
        self.score = score
