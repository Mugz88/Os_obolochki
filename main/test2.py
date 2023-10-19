drag = ['/home/sany/Документы/stud/Os_obolochki/Baza/Doc','/home/sany/Документы/stud/Os_obolochki/Baza/ProgramFile','/home/sany/Документы/stud/Os_obolochki/Baza/ProgramFile/Без имени 1', '/home/sany/Документы/stud/Os_obolochki/Baza/ProgramFile','/home/sany/Документы/stud/Os_obolochki/Baza/ProgramFile/Без имени 2'  ]
for i in range(len(drag)):
    buffi = [i for i in drag[i].split('/') if i]
    j = i
    while j < len(drag):
        
        buffj = [i for i in drag[j].split('/') if i]
        for word in buffj[:-1]:    
            if buffi[-1] == word:
                bl = drag[i]
                drag[i] = drag[j]
                drag[j] = bl
        j+=1
print(drag)
