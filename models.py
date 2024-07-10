from mongoengine import Document, StringField, IntField, ListField, connect

class Cheater(Document):
    userName = StringField(unique=True)
    rank = IntField(unique=True)
    questionLink = StringField()
    contestId = StringField()

class Contest(Document):
    name = StringField()
    question3 = ListField()
    question4 = ListField()

class Solution(Document):
    rank = IntField(unique=True)
    solution = StringField()
    contestId = StringField()
