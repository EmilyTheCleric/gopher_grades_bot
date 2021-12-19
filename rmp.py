import ratemyprofessor
import time

def get():
    file = open("temp_data.eri","r")
    lines = file.read().split('\n')
    file.close()
    prof_names = set()
    instructor_lines = {} #name -> [line_indexes]
    for i in range(len(lines)):
        try:
            if lines[i][0] =='c':#we don't care about classes
                continue
            else:
                name = get_name(lines[i])
                prof_names.add(name)#add prof name to set
                try:#add line to prof_names dictionary
                    instructor_lines[name].append(i)
                except:
                    instructor_lines[name] = [i]
                    
        except:
            print(lines[i])
##    prof_names.remove("None")
    
    school = ratemyprofessor.get_school_by_name("University of Minnesota Twin")#get umn tc
    
    print(len(prof_names))#debug to see how many names
    for name in prof_names:
        rmp_data = ratemyprofessor.get_professor_by_school_and_name(school, name)#get the professor
        indexes = instructor_lines[name]#get all the indexes for lines that professor appears on
        for i in indexes:
            line = lines[i]#get line
            if name != "None":
                if(rmp_data):
                    if(rmp_data.rating):#add rating score
                        line+=','+str(rmp_data.rating)
                    else:
                        line+=',N/A'
                    if(rmp_data.difficulty):#add dificulty score
                        line+=","+str(rmp_data.difficulty)
                    else:
                        line+=",N/A"
                else:
                    line+=',N/A,N/A'
            else:
                line+=',N/A,N/A'
            lines[i]=line#overwrite line

    #write to file
    file = open("data.eri","w")
    file.write('\n'.join(lines))
    file.close()
    get_avg_gpa_classes()
    
    print("done")
    
def get_name(line):
    return line.split(':')[1].split(',')[0]

        
def get_avg_gpa_classes():
    file = open("data.eri","r")
    lines=file.read().split('\n')
    file.close()
    prev_class_line =""
    for i in range(len(lines)):    #go through data.eri
        try:#otherwise, add rating and difficulty scores to instructors
            line=lines[i]
            words = line.split(",")
            n = words[0].split(":")
            if n[0] == 'i':
                name = n[1]
                
                rate = words[6]
                diff = words[7]
                try:
                    class_avg_rat+=float(rate)
                    class_avg_diff+=float(diff)
                    num_profs+=1
                except:
                    pass
            elif n[0]=='c':
                line=lines[i]
                if(prev_class_line==""):
                    prev_class_line=line
                    class_avg_rat=0
                    class_avg_diff=0
                    class_index=i
                    num_profs=0
                    lines.append(line)
                    continue
                try:
                    class_avg_rat/=num_profs
                    class_avg_diff/=num_profs
                except:
                    class_avg_rat="N/A"
                    class_avg_diff="N/A"
                prev_class_line+=','+truncate(class_avg_rat,2)+','+truncate(class_avg_diff,2)
    ##            print(prev_class_line)
                lines[class_index]=prev_class_line

                class_avg_diff=0
                class_avg_rat=0
                class_avg_diff=0
                prev_class_line=line
                num_profs=0
                class_index=i
            
        except:
            pass
##            print(line)
##            print(i)
##            print(len(lines))
##            lines.append(lines[i])
    file = open("data.eri","w")
    file.write('\n'.join(lines))
    file.close()
    

def truncate(f, n):
    if(f==0 or f=="N/A"):
        return "N/A"
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])



