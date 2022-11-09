import os
import sys
import ast
import random
import copy


def createxam(inputfile = [], outputfile = [], mainheadingtext = [], secondheadingtext = [], instructiontext = []):
    
    examheader = ['<!DOCTYPE HTML>\n<html lang="en">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n',
    '<link href=\'http://fonts.googleapis.com/css?family=Open+Sans\' rel=\'stylesheet\' type=\'text/css\'>\n\n',
    '<title>Exam</title>\n',
    '<style type="text/css">\n<!--\n.Exam {\n\tcounter-reset: term;\n}\n',
    '.IDInfo {font-size:12px; font-style: normal; font-weight: normal; font-variant: normal; text-align: right; padding-bottom: 18px; font-family: \'Open Sans\', sans-serif;}\n',
    '.HeadingInfo {font-size:12px; font-style: normal; font-weight:600; font-variant: normal; text-align: center; line-height: 1.5em;font-family: \'Open Sans\', sans-serif;}\n',
    '.Instruc {font-size:12px; font-style: normal; font-weight: normal; font-variant: normal; text-align: left; margin-bottom: 0.5em; font-family: \'Open Sans\', sans-serif;}\n\n',
    '.Question:before {counter-increment: term; content: counter(term) ". ";}\n',
    '.Set { page-break-inside:avoid;}\n',
    '.Question {font-size:12px; font-style: normal; font-weight: normal; font-variant: normal; text-align: left; padding-left: 20px ; text-indent: -19px ; margin-bottom: 0em; font-family: \'Open Sans\', sans-serif;}\n',
    '.Answer {font-size:12px; font-style: normal; font-weight: normal; font-variant: normal; text-align: left; margin-top: 0.2em; font-family: \'Open Sans\', sans-serif;}\n',
    '.Correct {font-size: normal; font-weight: normal; text-indent: inherit; font-family: \'Open Sans\', sans-serif;}\n',
    '.Correct.hidden { font-size: Large; font-weight: Bold; text-indent: 40px; font-family: \'Open Sans\', sans-serif;}\n\n',
    '@media print {.button{display: none;}}\n-->\n</style>\n\n<script language="javascript">\nfunction changeText(idElement) {\n    var element = document.getElementById(\'element\' + idElement);\n    if (idElement === 1 || idElement === 2) {\n        if (element.innerHTML === \'Show Correct Answers\') {\n\t\telement.innerHTML = \'Hide Correct Answers\';  \n\t\tvar selects = document.getElementsByClassName("Correct");\n\t\tfor(var i =0, il = selects.length;i<il;i++){\n\t\t\tselects[i].className += " hidden";\n\t\t}\n        } else {\n\t\tlocation.reload();\n        }\n    }\n}\n</script>\n',
    '</head>\n\n<body>\n\n<button class="button" id="element1" onClick="javascript:changeText(1)">Show Correct Answers</button>\n\n',
    
    '<p class="IDInfo">Name:__________________________________________</p>\n',
    
    '<p class="IDInfo">Student I.D.#:__________________________________________</p>']
    
    if (os.path.isfile(inputfile)):
        
        # Read in file
        dcontents = 0
        with open(inputfile, 'r') as file:
            dcontents = file.read().replace('\n', '')
            
        # consider the text as a list
        masterlist = ast.literal_eval(dcontents)
        questionlist = []
        sectionlist = []
            
        # Randomize the questions within each section
        # loop through each section
        for cM in range(len(masterlist)):   
            submasterlist = masterlist[cM]
            
            # randomly rearrange the questions
            for cS in range(random.randint(3, 10)): 
                random.shuffle(submasterlist)
                
            subsectionlist = [cM] * len(submasterlist)
            sectionlist = sectionlist + subsectionlist
            questionlist = questionlist + submasterlist
                    
        # The questions now have a random order within each section
        # Randomize answers using constrained sequences
        newsequence = [[1, 0, 1, 2, 3, 2, 0, 3],
                       [1, 0, 3, 2, 1, 2, 3, 0],
                       [1, 0, 0, 1, 3, 2, 2, 3],
                       [1, 1, 0, 3, 3, 0, 2, 2],
                       [1, 2, 0, 1, 3, 3, 2, 0],
                       [1, 2, 3, 0, 1, 2, 3, 0],
                       [1, 3, 2, 0, 2, 0, 1, 3],
                       [1, 3, 1, 3, 2, 0, 0, 2],
                       [2, 0, 3, 2, 3, 1, 0, 1],
                       [2, 0, 1, 2, 3, 0, 3, 1],
                       [3, 1, 0, 2, 0, 3, 1, 2],
                       [3, 2, 1, 1, 2, 0, 3, 0],
                       [3, 2, 1, 0, 3, 0, 1, 2],
                       [3, 2, 2, 1, 0, 0, 3, 1],
                       [3, 3, 2, 1, 2, 1, 0, 0]]
        # each newsequence has 120 
        while (len(questionlist) > (len(newsequence)*8)):
            newsequence = newsequence + newsequence
        
        # randomly reverse some sequences
        for cS in range(len(newsequence)):
            if (random.randint(0, 99) > 50):
                newsequence[cS].reverse()
        
        # randomly shuffle the sequences
        for cS in range(random.randint(3, 10)): 
            random.shuffle(newsequence)
        
        # collapse the sequence into one list
        sequence = [item for sublist in newsequence for item in sublist]
            
        # Randomize answers
        for cQ in range(len(questionlist)):   
            question = copy.deepcopy(questionlist[cQ])
            answers = copy.deepcopy(question[1])
            # if it is the correct answer tag it with the class
            for cA in range(len(answers)):
                if cA == 0:
                    answers[cA] = '<li class="Correct">%s</li>' % (answers[cA])
                else:
                    answers[cA] = '<li>%s</li>' % (answers[cA])
                    
            # shuffle the incorrect answers
            newanswers = [0] * len(answers)
            correctanswer = copy.deepcopy(answers[0])
            incorrectanswers = copy.deepcopy(answers[1:len(answers)])
            for cS in range(random.randint(3, 10)): 
                random.shuffle(incorrectanswers)
                
            # for questions with less than or more than 4, just use a random
            if (len(answers) != 4):
                # special case
                speccase = [0,1,2,3,4]
                speccase = speccase[0:len(answers)]
                for cS in range(random.randint(3, 10)): 
                    random.shuffle(speccase)
                sequence[cQ] = copy.deepcopy(speccase[0])
            
            # place the answers in the right locations
            currentwrong = 0
            for cA in range(len(answers)):
                if (sequence[cQ] == cA):
                    newanswers[cA] = copy.deepcopy(correctanswer)
                else:
                    newanswers[cA] = copy.deepcopy(incorrectanswers[currentwrong])
                    currentwrong = currentwrong + 1
            
            # place the answers back with the question
            question[1] = copy.deepcopy(newanswers)
            questionlist[cQ] = copy.deepcopy(question)
                    
        # Write Exam HTML Header
        f = open(outputfile, 'w')
        for cQ in range(len(examheader)):
            f.write(examheader[cQ])
        
        
        f.write('<p class="HeadingInfo">%s<br />%s</p>' % (mainheadingtext, secondheadingtext))
        f.write('\n')
        f.write('<p class="Instruc"><strong>Instructions</strong>: There are %d questions. %s</p>' % (len(questionlist), instructiontext))
        f.write('\n<p class="Exam">\n\n')

        currentsection = 0
        # Write each question
        for cQ in range(len(questionlist)):   
            question = questionlist[cQ]

            if (cQ == 0) and (currentsection == 0):
                f.write('<div> <!--    Section %d     -->\n' % (currentsection+1))
            else:
                if sectionlist[cQ] != currentsection:
                    currentsection = sectionlist[cQ]
                    f.write('\n</div>\n\n<div> <!--    Section %d     -->\n' % (currentsection+1))
                    
            f.write('\n\t<div class="Set">\n')
            f.write('\t\t<p class="Question">%s</p>\n' % (question[0]))
            f.write('\t\t<ol type="a" class="Answer">\n')
            answers = question[1]
            for cA in range(len(answers)):
                f.write('\t\t\t%s\n' % (answers[cA]))
            f.write('\t\t</ol>\n\t</div>\n')
        
        f.write('\n</div>\n</body>\n</html>')
        f.close() # Close file
        


if __name__ == "__main__":
                
    os.chdir(os.path.dirname(sys.argv[0]))
    
    createxam(inputfile = 'Questions.txt',  outputfile = 'Course_X_Exam1_Form1A.html', 
              mainheadingtext = 'Course X: Course Title', secondheadingtext = 'Exam 1 - Form 1A',
              instructiontext = 'For each question please select the answer that is most appropriate. Each question is worth 2 points.')
    
    createxam(inputfile = 'Questions.txt',  outputfile = 'Course_X_Exam1_Form2B.html', 
              mainheadingtext = 'Course X: Course Title', secondheadingtext = 'Exam 1 - Form 2B',
              instructiontext = 'For each question please select the answer that is most appropriate. Each question is worth 2 points.')
    
