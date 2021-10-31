import discord
from discord.ext import commands
from prettytable import PrettyTable
from tabulate import tabulate
from secrets import TOKEN

class course:
    def __init__(self,name, instructors, students, sections, gpa): #for the entire course
        self.name = name
        self.instructors = instructors
        self.students = students
        self.sections=sections
        self.gpa=gpa
    def __eq__(self,oth):
        return self.name == oth.name
    def __str__(self):
        return self.name + ', ' + str(self.students)+', '+str(self.sections)+', '+str(self.gpa)

class instructor_course:
    def __init__(self,name, course_name, students, sections,GPA_PM,gpa,rating,difficulty):    #for instructors in the course
        self.name = name
        self.course_name = course_name
        self.students = students
        self.sections = sections
        self.rating = rating
        self.difficulty = difficulty
        self.gpaPM=GPA_PM
        self.gpa=gpa
    def __str__(self):
        return  self.name + ', '+ str(self.students) +', ' +str(self.sections)+', '+str(self.gpaPM)+', '+ str(self.gpa) #debugging
    def __lt__(self,oth):
        return self.gpa > oth.gpa #for sorting purposes

def read_from_file():                           #file made by another program from entire dataset
    file = open('data.eri','r')                 #stored in .eri files, aka my initials B)
    lines = file.read() 
    lines = lines.split('\n')                  #read_lines doesn't remove \n, fucks with whole progrm
    file.close()
    for line in lines:                          #go through all the lines
        words = line.split(':')
        if words[0] == 'c':                     #if its a class
            data = words[1].split(',')
            nc = course(data[0],[],data[1],data[2],data[3])#get data, make course object
            course_lst[data[0]] = nc                        #add it to the dic of courses
        elif words[0] == 'i':           #if its an instructor
            try:  
                data = words[1].split(',')      
                ni = instructor_course(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) #get data
                course_lst[data[1]].instructors.append(ni)                                          #add to the list of instructors for a course
            except:
                try:                                                        #if no rating, put '-'
                    data = words[1].split(',')
                    ni = instructor_course(data[0],data[1],data[2],data[3],data[4],data[5],"-","-")
                    course_lst[data[1]].instructors.append(ni)
                except:                                                 #if not enough data, don't care about it
                    pass

#### Set up bot so we can start adding commands
client = commands.Bot(command_prefix='!')

@client.command()
async def gpa(ctx,*arg):                                            #gpa command
    print(arg)  
    if len(arg) == 0:
        await ctx.send("please input a class as well")              #error message if only !gpa sent
        return
    else:
        if len(arg) == 2:                                   #could be !gpa csci 2041 or !gpa csci2041, either one works cuz im good at programming
            try:
                int(arg[1])
                course = arg[0].upper() + arg[1].upper()
            except:
                course = arg[0].upper()
        else:
            course = arg[0].upper()
        try:
            tables = []                                     #the tables to be printed
            curr_tables = 0
            table = [["Instructors", "Students", "Sections", "GPA±","GPA","Rating/5","Difficulty/5"]]#headers
            c=course_lst[course]#get course data
            i = course_lst[course].instructors#get all the instructors
            i.sort()#sort from best to worst
            table.append(["All Instructors", c.students, c.sections, '-', c.gpa, '-', '-']) #add first line to table

            for a in i:
                to_say =  a.__str__()
                if len(tabulate(table,tablefmt="plain")) >= 1700: #if the message gets too big
                    tables.append(table)                          #split it into diff tables and diff messages (rare, happens with math1372)
                    table = [["Instructors", "Students", "Sections", "GPA±","GPA","Rating/5","Difficulty/5"]]
                if a.name == '':
                    a.name = 'Unknown Instructor'                 #sometimes instructors aren't listed, so this is shown(ex stat3021 almost no names for some reason)
                table.append([a.name, a.students, a.sections, a.gpaPM, a.gpa,a.rating,a.difficulty])
            tables.append(table)
            for t in tables:
                await ctx.send('```'+tabulate(t,tablefmt="plain")+'```')#send all tables (```makes it monospaced (important for tables))
        except:
            await ctx.send('error, no course named '+course+' found or not enough data to get gpa')


course_lst = {}                             #name -> course_object
read_from_file()                            #initialize data
print(len(course_lst.keys()))                #should be 6619




client.remove_command("help")#auto help command is kinda bad

async def rmp(ctx,arg):
    pass
    #take proffessor's name
    #output: rating, difficulty, retake%, top comment


@client.command()
async def help(ctx,*arg):
    to_say = '!gpa [CLASS]: shows the average gpa of all proffesors and TA\'s in that class ex: !gpa CSCI2021\nall data from:gophergrades.com and github.com/DannyG72/UMN-Grade-Dataset'
    to_say += "\nall ratings and difficulty gathered from rate my proffessor"#give credit
    to_say += "\n(if a prof's data/rating seems to be wrong @Emilbee#9025 on discord)"
    await ctx.send(to_say)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
