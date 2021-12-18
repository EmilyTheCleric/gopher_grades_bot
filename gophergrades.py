import openpyxl
from pathlib import Path

class course: #each course has the following attributes:
    def __init__(self,name, instructors, students, sections, gpa):
        self.name = name.replace('ʻ',"'").replace(',',' ')
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
        self.name = name.replace('ʻ',"'").replace(',',' ')
        self.course_name = course_name.replace('ʻ',"'").replace(',',' ')
        self.students = students
        self.sections = sections
        self.gpaPM=GPA_PM
        self.gpa=gpa
    def __str__(self):
        return  self.name + ','+ self.course_name+','+ str(self.students) +',' +str(self.sections)+','+str(self.gpaPM)+','+ str(self.gpa)

def write_data():
##    global lines  
##    file = open('gg.csv','r') #open file we made in clean_me
##    lines = file.readlines()
##    file.close()
##    get_sects()             #get dictionary of sections
##    get_courses()           #get dictionary of courses
##    get_instructs()         #get all instructors
    to_save = ''
    for c in course_lst.values():               #save course
        to_save += 'c:'+c.__str__() +'\n'
        for i in c.instructors:
            to_save += 'i:'+i.__str__() +'\n'   #save instructors
    file = open('temp_data.eri','w')
    file.write(to_save)                     #save to file
    file.close()

wb_obj = openpyxl.load_workbook("Copy of raw_grade_data_summer2017_fall2020-1.xlsx", read_only=True) 
course_lines_dic = {}
course_lst = {} #list of all courses
gpa_dic={'A':4,'A-':3.7,'B+':3.3,'B':3,"B-":2.7,"C+":2.3,'C':2,'C-':1.7,'D+':1.3,'D':1,'F':0}
course_name_list = []
course_instr_duo = {}#course,instr,term->lines
course_instr_lst = []#course-instr,term
validGrades = ['A','A-','B+','B','B-','C+','C','C-','D+','D','F']


# Read the active sheet:
sheet = wb_obj.active


#make dictionaries of instructorName->rows with them and courseName
def get_sects():
    i=0
    for row in sheet.iter_rows():
        if(i==0):
            i+=1
            continue
    ##    print(row)
        try:
        #TERM,TERM_DESCR,INSTITUTION,CAMPUS,SUBJECT,CATALOG_NBR,CLASS_SECTION,DESCR,CRSE_GRADE_OFF,CLASS_HDCNT,GRADE_HDCNT,INSTR_ROLE,HR_NAME,JOBCODE_DESCR
            subjectName=row[4].value+row[5].value
    ##        print(subjectName)
            prof_name =get_prof_name(str(row[12].value))
            name_instr = subjectName+'-'+prof_name
            if not subjectName in course_name_list:
                course_name_list.append(subjectName)
            if not name_instr in course_instr_lst:
                course_instr_lst.append(name_instr)
            if (row[8].value in validGrades):
                    try:
                        course_lines_dic[subjectName].append(row)
                        try:
                            course_instr_duo[name_instr].append(row)
                        except:
                            course_instr_duo[name_instr] = [row]
                    except:
                        course_lines_dic[subjectName] = [row]
                        course_instr_duo[name_instr] = [row]
        except:
##            pass
            print(row)

def get_courses():
    current_teacher = []
    for course_name in course_name_list:
        try:
            rows = course_lines_dic[course_name]
        except:
##            print(course_name)
            continue
        students = 0
        sections = []
        for row in rows:
            students += int(row[10].value)
            prof_name =get_prof_name(str(row[12].value))
            if not((row[6].value+'-'+row[1].value+'-'+prof_name ) in sections):
                sections.append(row[6].value+'-'+row[1].value+'-'+prof_name)
        gpa = get_gpa(rows,students)
        course_lst[course_name] = (course(course_name,[],students,len(sections),truncate(gpa,2)))

def get_instructs():
    for inst in course_instr_lst:
        try:
            rows = course_instr_duo[inst]
        except:
##             print(inst)
             continue
        students = 0
        sections = []
        name = ''
        for row in rows:
            name = row[4].value + row[5].value
            students += int(row[10].value)
            prof_name =get_prof_name(str(row[12].value))
            if not((row[6].value+'-'+row[1].value+'-'+prof_name ) in sections):
                sections.append(row[6].value+'-'+row[1].value+'-'+prof_name)
        gpa = get_gpa(rows,students)
        c = course_lst[name]
        gpapm = gpa - c.gpa
        prof_name =get_prof_name(str(row[12].value))
        c.instructors.append(instructor_course(prof_name,name,students,len(sections),truncate(gpapm,2),truncate(gpa,2)))

#fixes Daniel J Challou PhD (now just Daniel Challou)
#actually fixed this while in his 4131 lecture LMAO
def get_prof_name(rawname):
    prof_name_wr_order = rawname.replace("PhD","").replace(','," ")
    prof_name =" ".join(prof_name_wr_order.split(' ')[1:]+prof_name_wr_order.split(' ')[0:1])
    if(len(prof_name.split(" "))>2):
        first_name = ""
        last_name =""
        for name in prof_name.split(" "):
            if(first_name =="" and name !="" and name != " "):
                first_name = name
            if(name!="" and name !=" "):
                last_name = name
        return first_name +" "+last_name
    return prof_name
    

def get_gpa(rows,studs):      #input: a list or lines with the same prof, output: gpa
    GPA = 0
    if studs == 0:
        return 0
    for row in rows:
        GPA += (gpa_dic[row[8].value]*(int(row[10].value)/studs))
    return GPA

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))
##
##get_sects()
##print('got sects')
##get_courses()
##print('got courses')
##get_instructs()
##print('got instructors')
##c = course_lst['MATH1372']
##print(c)
##write_data()
