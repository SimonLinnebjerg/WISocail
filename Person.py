
class Person:
    def __init__(self, name, friends, summary, review):
        self.name = name
        self.friends = friends
        self.summary = summary
        self.review = review

    def __init__(self, name):
        self.name = name
        self.friends = []
