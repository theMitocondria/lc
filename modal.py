from Models.Step1 import Step1;
from Models.Step2 import Step2;
from Utils.Timer import timer_annotation;

code1 = ""
code2 = ""

final_output = Step2(Step1(code1) , Step1(code2))
print(final_output)

