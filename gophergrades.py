class course: #each course has the following attributes:
    def __init__(self,name, instructors, students, sections, gpa):
        self.name = name
        self.instructors = instructors
        self.students = students
        self.sections=sections
        self.gpa=gpa
    def __eq__(self,oth):
        return self.name == oth.name
    def __str__(self):
        return self.name + ',' + str(self.students)+','+str(self.sections)+','+str(self.gpa)

class instructor_course:#each instructor has the following attributes:
    def __init__(self,name, course_name, students, sections,GPA_PM,gpa):
        self.name = name
        self.course_name = course_name
        self.students = students
        self.sections = sections
        self.gpaPM=GPA_PM
        self.gpa=gpa
    def __str__(self):
        return  self.name + ','+ self.course_name+','+ str(self.students) +',' +str(self.sections)+','+str(self.gpaPM)+','+ str(self.gpa)
##    def to_file(self)

##file = open('gg.csv','r')
##lines = file.readlines()
##file.close()
#12 and 13
course_lines_dic = {}
course_lst = {} #list of all courses
gpa_dic={'A':4,'A-':3.7,'B+':3.3,'B':3,"B-":2.7,"C+":2.3,'C':2,'C-':1.7,'D+':1.3,'D':1,'F':0}
course_name_list = []
course_instr_duo = {}#course,instr,term->lines
course_instr_lst = []#course-instr,term

lines=''

def write_data():
    global lines  
    file = open('gg.csv','r') #open file we made in clean_me
    lines = file.readlines()
    file.close()
    get_sects()             #get dictionary of sections
    get_courses()           #get dictionary of courses
    get_instructs()         #get all instructors
    to_save = ''
    for c in course_lst.values():               #save course
        to_save += 'c:'+c.__str__() +'\n'
        for i in c.instructors:
            to_save += 'i:'+i.__str__() +'\n'   #save instructors
    file = open('temp_data.eri','w')
    file.write(to_save)                     #save to file
    file.close()

def read_from_file(): #vestigial debugging
    file = open('data.eri','r')
    lines = file.read()
    lines = lines.split('\n')
    file.close()
    for line in lines:
        words = line.split(':')
        if words[0] == 'c':
            data = words[1].split(', ')
            nc = course(data[0],[],data[1],data[2],data[3])
            course_lst[data[0]] = nc
        elif words[0] == 'i':
            data = words[1].split(', ')
            ni = instructor_course(data[0],data[1],data[2],data[3],data[4],data[5])
            course_lst[data[1]].instructors.append(ni)
            
    

def get_sects():  
    for line in lines:
        try:
            words = line.split(',')
            name = words[4] + words[5]
            name_instr = name +'-'+words[12]
            if not name in course_name_list:
                course_name_list.append(name)
            if not name_instr in course_instr_lst:
                course_instr_lst.append(name_instr)
            if (words[8] in grade):
                try:
                    sects = course_lines_dic[name]
                    sects.append(line)
                    course_lines_dic[name] = sects
                    try:
                        sits = course_instr_duo[name_instr]
                        sits.append(line)
                        course_instr_duo[name_instr]
                    except:
                        course_instr_duo[name_instr] = [line]
                except:
                    course_lines_dic[name] = [line]
                    course_instr_duo[name_instr] = [line]
        except:
            pass
##            print(line)

grade = ['A','A-','B+','B','B-','C+','C','C-','D+','D','F']
def get_courses():
    current_teacher = []
    for course_name in course_name_list:
        try:
            ls = course_lines_dic[course_name]
        except:
##            print(course_name)
            continue
        students = 0
        sections = []
        for l in ls:
            words = l.split(',')
            students += int(words[10])
            if not((words[6]+'-'+words[0]+'-'+words[12] ) in sections):
                sections.append(words[6]+'-'+words[0]+'-'+words[12])
        gpa = get_gpa(ls,students)
        course_lst[course_name] = (course(course_name,[],students,len(sections),truncate(gpa,2)))

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))

def get_instructs():
    for inst in course_instr_lst:
        try:
            ls = course_instr_duo[inst]
        except:
##             print(inst)
             continue
        students = 0
        sections = []
        name = ''
        for l in ls:
            words = l.split(',')
            name = words[4] + words[5]
            students += int(words[10])
            if not((words[6]+'-'+words[0]+'-'+words[12] ) in sections):
                sections.append(words[6]+'-'+words[0]+'-'+words[12])
        gpa = get_gpa(ls,students)
        c = course_lst[name]
        gpapm = gpa - c.gpa
        c.instructors.append(instructor_course(words[12],name,students,len(sections),truncate(gpapm,2),truncate(gpa,2)))

def get_gpa(lst,studs):      #input: a list or lines with the same prof, output: gpa
    GPA = 0
    if studs == 0:
        return 0
    for line in lst:
        words = line.split(',')
        GPA += (gpa_dic[words[8]]*(int(words[10])/studs))
    return GPA
##get_sects()
##print('got sects')
##get_courses()
##print('got courses')
##get_instructs()
##print('got instructors')
####read_from_file()
##c = course_lst['MATH1372']
##print(c)
##write_data()
    


