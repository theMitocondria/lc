from mongoengine import Document, StringField, IntField, ListField, connect

class Cheater(Document):
    userName = StringField()
    rank = IntField()
    questionLink = StringField()
    contestId = StringField()

class Contest(Document):
    name = StringField()
    question3 = ListField()
    question4 = ListField()

class Solution(Document):
    rank = IntField()
    solution = StringField()
    contestId = StringField()
