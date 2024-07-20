from Models.Step1 import Step1;
from Models.Step2 import Step2;
from Contants import code3
from Contants import code4


def checkPlagPercentage (code2, questionId) :
    if questionId == '4' : 
        final_output = Step2(code4, Step1(code2))
    elif questionId == '3' :
        final_output = Step2(code3, Step1(code2))

    return final_output
