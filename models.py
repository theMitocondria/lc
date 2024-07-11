from mongoengine import Document, StringField, IntField, ListField, connect
from Contants import (code3, code4)
class Cheater(Document):
    userName = StringField()
    rank = IntField()
    questionLink = StringField()
    contestId = StringField()

class Contest(Document):
    name = StringField()
    question3 = ListField()
    question4 = ListField()
    cheated3Sol = StringField(default=code3)
    cheated4Sol = StringField(default=code4)

class Solution(Document):
    rank = IntField()
    solution = StringField()
    contestId = StringField()
    solutionNumber = IntField()
    
