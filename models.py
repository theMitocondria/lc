from mongoengine import Document, StringField, FloatField , ListField, IntField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, connect

class Solution(Document):
    code = StringField(required=True)

class Cheater (EmbeddedDocument) :
    name_of_cheater = StringField(required=True)
    plagpercentage =  FloatField(required = True)
    rank = IntField(required=True)
    code = ReferenceField(Solution, required=True)
class CheaterArray(Document):
    array_of_cheaters = ListField(EmbeddedDocumentField(Cheater))

class Contest(Document):
    name = StringField(required=True)
    question3 = ReferenceField(CheaterArray, required=True)
    question4 = ReferenceField(CheaterArray, required=True)
    cheated3Sol = ReferenceField(Solution) 
    cheated4Sol = ReferenceField(Solution)


#contest creation ka tarika : 
    # create code3,code4 solution
    # then apna create contest with ref of sol3 , sol4 do from postman

