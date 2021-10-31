#things wrong in dataset.csv:
#class nums can be "1,042", instead of just 1042
#classes with commas in the name
#prof's name in quotes
#also we want firstname lastname not lastname firstname
#fixes:

def clean_file(fname):
    file = open(fname,'r')
    lines = file.read()
    lines = lines.split('\n')
    file.close()
    new_lines = []
    for line in lines:
        words = line.split('"')
##        if "Intro to Thermo" in line:
##            print(len(words))
        if len(words) == 5: #ideal len: 1
            num = words[1].split(',')
            if len(num) == 2:
##                print(line)
                n2 = num[0]+num[1]
                try:                              #this is for  numbers over 1k aka "1,042" to delete commas
                    int(n2)
##                    print(line)
                    name = words[3]
                    name = name.split(',')
                    name = name[1]+' '+name[0]
                    nl=words[0]
                    for i in range(1,len(words)):
                        if i == 1:
                            nl+=n2
                        elif i ==3:
                            nl+=name
                        else:
                            nl+=words[i]
##                    print(nl)
                    new_lines.append(nl)
##                    for i in range(1,len(words)):
##                        if i == 1:
##                            nl+=n2
##                        else:
##                            nl+=words[i]+'"'
##                    print(nl)
##                    new_lines.append(nl)
                
                except:                         # I believe this one takes commas out of titles/names out of profs
                    n2 = num[0]+num[1]
                    name = words[3]
                    name = name.split(',')
                    name = name[1]+' '+name[0]
                    nl=words[0]
                    for i in range(1,len(words)):
                        if i == 1:
                            nl+=n2
                        elif i ==3:
                            nl+=name
                        else:
                            nl+=words[i]
##                    print(nl)
                    new_lines.append(nl)
            elif (len(num)==3):             #prof's name is in quotes and has middle name
                n2 = num[0]+num[1]+num[2]
                name = words[3]
                name = name.split(',')
                name = name[1]+' '+name[0]
                nl=words[0]
                for i in range(1,len(words)):
                    if i == 1:
                        nl+=n2
                    elif i ==3:
                        nl+=name
                    else:
                        nl+=words[i]
##                    print(nl)
                new_lines.append(nl)
                
            else:
                new_lines.append(line)

        elif len(words) == 3:             #prof's name is in quotes
            name = words[1]
            name = name.split(',')
            name = name[1]+' '+name[0]
            nl=words[0]
            for i in range(1,len(words)):
                if i ==1:
                    nl+=name
                else:
                    nl+=words[i]
##                    print(nl)
            new_lines.append(nl)
        elif len(words)==7:                 #over 1k students and grades ex "2,033" students and "1,965" got an A
            num = words[1].split(',')
            num2 = words[3].split(',')
##            print(line)
##            print(len(num),len(num2))
            if len(num) == len(num2) and len(num) == 2:
               
                n2 = num[0]+num[1]
                n3 = num2[0]+num2[1]
                name = words[5]
                name = name.split(',')
                name = name[1]+' '+name[0]
                nl=words[0]
                for i in range(1,len(words)):
                    if i == 1:
                        nl+=n2
                    elif i ==3:
                        nl+=n3
                    elif i == 5:
                        nl+=name
                    else:
                        nl+=words[i]
##                print(nl)
                new_lines.append(nl)
                                                                          #0                      #1 num   #num2       
            else: #for this one line: 1189,Fall 2018,UMNTC,UMNTC,PHYS,8012,001,Quant Field Thy II,A,10,6,PI,"Shifman,Mikhail ""Misha""",Professor
##                print(line)
                name = num[0] +' "'+ num2[0] +'" '+ num[1]
                nl=words[0]
                for i in range(1,len(words)):
                    if i == 1:
                        nl+=name
                    if i ==3:
                        pass
                    else:
                        nl+=words[i]
##                print(nl)
                new_lines.append(nl)
        else:
            new_lines.append(line)
    printing_lines = []
    for line in new_lines: #removes middle names
        words=line.split(',')
        name = words[12]
        names = name.split(" ")
        if len(names) == 3:
            name = names[0] + ' ' + names[2]
        else:
            name = ' '.join(names)
        to_add = words[0]
        for i in range(1,len(words)):
            if i == 12:
                to_add += ',' +name
            else:
                to_add += ',' +words[i]
        printing_lines.append(to_add)
##    print('fin')
    new_lines = '\n'.join(printing_lines)
    file = open('gg.csv','w')
    file.write(new_lines)
    file.close()
    
##    print('wrote')
##clean_file("dataset.csv")
