import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
from prettytable import PrettyTable
from tabulate import tabulate
from datetime import datetime, timedelta
from secrets import TOKEN

DATA_FILE, PREFIX_FILE, REMINDERS_FILE = "data.eri", "prefixes.txt", "reminders.txt"

class course:
    def __init__(self,name, instructors, students, sections, gpa,rating,difficulty): #for the entire course
        self.name = name
        self.instructors = instructors
        self.students = students
        self.sections=sections
        self.gpa=gpa
        self.rating=rating
        self.difficulty=difficulty
    def __eq__(self,oth):
        return self.name == oth.name
    def __str__(self):
        return self.name + ', ' + str(self.students)+', '+str(self.sections)+', '+str(self.gpa)+', '+str(self.rating)+", "+str(Self.difficulty)

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
    with open(DATA_FILE) as file:
        lines = [line.rstrip() for line in file]
    for line in lines:                          #go through all the lines
        words = line.split(':')
        if words[0] == 'c':                     #if its a class
            data = words[1].split(',')
            try:
                nc = course(data[0],[],data[1],data[2],data[3],data[4],data[5])#get data, make course object
            except:
                nc = course(data[0],[],data[1],data[2],data[3],'-','-')#get data, make course object
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

##########Following code based on: https://stackoverflow.com/questions/56796991/discord-py-changing-prefix-with-command

def read_prefixes():
    with open(PREFIX_FILE) as file:
        lines = [line.rstrip() for line in file]
    prefixes={}
    for line in lines:
        try:
            gid = int(line.split(',')[0])
            prefix=line.split(',')[1]
            prefixes[gid]=prefix
        except:
            print(line)
    return prefixes
              
custom_prefixes = read_prefixes()


#You'd need to have some sort of persistance here,
#possibly using the json module to save and load
#or a database                
default_prefixes = ['!']

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

course_lst = {}                             
read_from_file()                            
print(len(course_lst.keys()))                
client =commands.Bot(command_prefix = determine_prefix) 

@client.command(brief = "sets a custom prefix for the server",
                help="""syntax:
                            setprefix <new_prefix>""")
@commands.guild_only()
@has_permissions(administrator=True)
async def setprefix(ctx, *, prefixes=""):
    if(not len(prefixes.split(" "))==1):
       await ctx.send("Error, prefixes can not have spaces")
       return
    alterPrefixFile(ctx.guild.id,(prefixes.split() or default_prefixes)[0])
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefix set!")

#we wanna change guild id if its in file, otherwise add it
def alterPrefixFile(gid,prefix):
    file = open("prefixes.txt",'r')
    lines=file.read().split('\n')#get lines
    file.close()
    found = False
    for line in lines:#iterate through lines
        data=line.split(',')
        if data[0] == str(gid):#if we found the guild id
            found=True
            lines.remove(line)
            data[1]=prefix
            lines.append(",".join(data))#change the prefix
            break
    if not found:#otherwise add it to the end
        lines.append(str(gid)+','+prefix)
    newFile='\n'.join(lines)
    file=open('prefixes.txt','w')#write a new file
    file.write(newFile)
    file.close()
    
    
######################End taken code

@client.command(brief = "see the average gpa and rate my professor scores for proffessors teaching a certain class",
                help="""syntax:
                            gpa <class> ex: !gpa csci2021""")
async def gpa(ctx,*arg):                                            #gpa command
    print(arg)  
    if len(arg) == 0:
        await ctx.send("please input a class as well")              #error message if only !gpa sent
        return
    else:
        if len(arg) == 2:                                   #could be !gpa csci 2041 or !gpa csci2041, either one works cuz im good at programming
            if arg[1][-1].upper()=='W':
                course=arg[0].upper()+arg[1].upper()
            else:
                try:
                    int(arg[1])
                    course=arg[0].upper()+arg[1]
                except:
                    course = arg[0].upper()
        else:
            course = arg[0].upper()
        try:
            tables = []                                     #the tables to be printed
            curr_tables = 0
            table = [["Instructors", "Students", "Sections", "GPA±","GPA","Rating/5","Difficulty/5"]]#headers
            c=course_lst[course]#get course data
            instructors = course_lst[course].instructors#get all the instructors
            instructors.sort()#sort from best to worst
            table.append(["All Instructors", c.students, c.sections, '-', c.gpa, c.rating, c.difficulty]) #add first line to table

            for proffessor in instructors:
                to_say =  proffessor.__str__()
                if len(tabulate(table,tablefmt="plain")) >= 1700: #if the message gets too big
                    tables.append(table)                          #split it into diff tables and diff messages (rare, happens with math1372)
                    table = [["Instructors", "Students", "Sections", "GPA±","GPA","Rating/5","Difficulty/5"]]
                if proffessor.name == '' or proffessor.name=="None":
                    proffessor.name = 'Unknown Instructor'                 #sometimes instructors aren't listed, so this is shown(ex stat3021 almost no names for some reason)
                table.append([proffessor.name, proffessor.students, proffessor.sections, proffessor.gpaPM, proffessor.gpa,proffessor.rating,proffessor.difficulty])
            tables.append(table)
            for table in tables:
                await ctx.send('```'+tabulate(table,tablefmt="plain")+'```')#send all tables (```makes it monospaced (important for tables))
        except:
            await ctx.send('error, no course named '+course+' found or not enough data to get gpa')


#######################################REMINDER CODE BELOW############################################################################

###adds a line to reminders.txt with info needed to send a reminder when the time comes
### that line stores info in the following way:
###author id, reminder text, server id, channel id, time to send,time values to wait
@client.command(brief = "sets a reminder and pings you at a certain time",
                help="""syntax:
                            remind <event> xx days yy hours zz minutes aa seconds""")
async def remind(ctx,*args): 
    times = [0,0,0,0] #days, hours, minutes, seconds
    words = list(args)

    positions_to_delete = []
    
    for i in range(len(words)): #for every word sent
        if words[i].lower() == 'me':
            positions_to_delete.append(i) #honestly I like saying remind me instead of remind so this makes sure its all good
        if words[i].lower() == 'day' or words[i].lower() == 'days': #get num of days and delete from args
            times[0] = int(words[i-1]) #get number of days
            positions_to_delete.append(i-1) #get position of number
            positions_to_delete.append(i) #get position of words
        if words[i].lower() == 'hour' or words[i].lower() == 'hours':#get num of hours and delete from args
            times[1] = int(words[i-1]) #get number of hours
            positions_to_delete.append(i-1) #get position of number
            positions_to_delete.append(i) #get position of words
        if words[i].lower() == 'minute' or words[i].lower() == 'minutes':#get num of minutes and delete from args
            times[2] = int(words[i-1])#get number of minutes
            positions_to_delete.append(i-1) #get position of number
            positions_to_delete.append(i) #get position of words
        if words[i].lower() == 'second' or words[i].lower() == 'seconds':#get num of seconds and delete from args
            times[3] =int(words[i-1])#get number of seconds
            positions_to_delete.append(i-1) #get position of number
            positions_to_delete.append(i) #get position of words

    positions_to_delete.reverse()
    
    for i in positions_to_delete: #delete the actual numbers and words of the reminder time
        words.pop(i)
    
    current_time = datetime.today()# get right now
    
    end_time = current_time + timedelta(days = times[0], hours = times[1], minutes = times[2], seconds = times[3])#add times
    
    reminder = ' '.join(words) #get whats left of the message (presumably the reminder)
    
    author = ctx.author.id #get author so we can @ them in message

    

    try:
        guild = str(ctx.guild.id) #check if bot in guild
    except:
        guild = None #otherwise in dm so no guild
        
    if times[0] + times[1] + times[2] + times[3] == 0:
        await ctx.send("please input a time")
        return

    #the following code sends a confirmation message


    message = 'I will remind you of your "'+str(reminder)+'" in' #base message
    
    #get times, makes it look pretty
    if times[0] > 0: #days
        if times[0] == 1: #single day with good grammer
            message += ' 1 day'
        else:               #multiple days
            message += ' '+ str(times[0])+' days'

    if times[1] > 0: #hours
        if times[1] == 1: #single hour with good grammer
            message += ' 1 hour'
        else:               #multiple hours
            message += ' '+ str(times[1])+' hours'

    if times[2] > 0: #minutes
        if times[2] == 1: #single minute with good grammer
            message += ' 1 minute'
        else:               #multiple minutes
            message += ' '+ str(times[2])+' minutes'

    if times[3] > 0: #seconds
        if times[3] == 1: #single second with good grammer
            message += ' 1 second'
        else:               #multiple seconds
            message += ' '+ str(times[3])+' seconds'

    for i in range(len(times)):
        times[i] = str(times[i])
    
    data = str(author) +','+ str(reminder) +','+ str(guild) +','+ str(ctx.channel.id) +','+ str(end_time) +','+ ';'.join(times) #gather all data to be stored

    await ctx.send(message) #send confirmation message
    
    
    
##    print(data)

    #add data to file
    file = open('reminders.txt','a')
    file.write(data+'\n')
    file.close()


    ##keep a log of all reminders sent, with some extra date :)
    unethical_spying_data = str(author)+','+str(ctx.author)+','+str(guild)+','+str(ctx.guild)+','+ str(ctx.channel.id)+','+str(ctx.channel)+','+str(reminder)+','+str(datetime.today())+','+ str(end_time) +','+ ';'.join(times)+'\n'
    file = open('unethical_spying.csv','a')
    file.write(unethical_spying_data)
    file.close()
            
    
### sends a list of all current reminders on the current channel and server with the same author  
@client.command(brief = "displays all reminders a user has",
                help="""syntax:
                            reminders""")
async def reminders(ctx):
    author = ctx.author #get author
    try:
        guild = ctx.guild.id #get guild if there is one
    except:
        guild = None #no guild if its a DM
    channel = ctx.channel.id # get channel 
    
    file = open('reminders.txt','r')
    reminders = file.read().split('\n')#author id, reminder text, server id, channel id, time to send
    file.close()

    active_reminders = []
    
    for reminder in reminders:  #go through all reminders in file
        data = reminder.split(',') #get data
        if str(author.id) == data[0] and str(guild) == data[2] and str(channel) == data[3]:#make sure author, guild, and channel is the same
            active_reminders.append(reminder) #if it is, add to active reminders
    
            
    if len(active_reminders) >0: #if users have active reminders
        message = ''
        for i in range(len(active_reminders)): #itterate through and gather data
##            try:
                data = active_reminders[i].split(',')
                time = data[4] #datetime stored as yyyy-mm-dd hh:mm:ss.ssssss

                YMD = time.split(' ')[0].split('-') #year month and day

                HMS = time.split(' ')[1].split(':') # hour minute and seconds

                remind_time = datetime(int(YMD[0]),int(YMD[1]),int(YMD[2]),int(HMS[0]),int(HMS[1]),int(HMS[2].split('.')[0]))#make date time for reminder time

                time = str (remind_time - datetime.today())

                formatted_time = []

                if 'day' in time or 'days' in time:
                    formatted_time.append(time.split(',')[0]) # this gets the day
                    HMS = time.split(',')[1].split(':')
                else:
                    HMS = time.split(':')

                if int(HMS[0]) == 1: #make hours pretty (exclude 0 hours, singular one hour)
                    formatted_time +=['1','hour']
                elif int(HMS[0]) > 1:
                    formatted_time +=[HMS[0],'hours']

                if int(HMS[1]) == 1: #make minutes pretty (exclude 0 minutes, singular one minute)
                    formatted_time +=['1','minute']
                elif int(HMS[1]) > 1:
                    formatted_time +=[HMS[1],'minutes']

                if int(round(float(HMS[2]))) == 1: #make seconds pretty (exclude 0 seconds, singular one second)
                    formatted_time +=['1','second']
                elif int(round(float(HMS[2]))) > 1:
                    formatted_time +=[str(round(float(HMS[2]))),'seconds']

                
                    
                    
                
                message += '\n[' + str(i) + '] "'+ data[1] +'" in: ' + ' '.join(formatted_time) #add reminder to message
        await ctx.send(message) #send list of reminders with time remaining
    else:
        await ctx.send("No reminders found")
##            except:
##                print(reminder)
        
@client.command(brief = "deletes a reminder the user had made before",
                help="""syntax:
                            delete <reminder index(s)> ex: !delete 0 4 2""")
async def delete(ctx,*args):
    nums = list(args)
    nums.sort()
    nums.reverse()
    
    author = ctx.author #get author
    try:
        guild = ctx.guild.id #get guild if there is one
    except:
        guild = None #no guild if its a DM
    channel = ctx.channel.id # get channel 
    
    with open(REMINDERS_FILE) as file:
        reminders = [line.rstrip() for line in file]

    active_reminders = []
    to_pop = []

##    print(reminders)
    
    for i in range(len(reminders)):  #go through all reminders in file
        data = reminders[i].split(',') #get data
        if str(author.id) == data[0] and str(guild) == data[2] and str(channel) == data[3]:#make sure author, guild, and channel is the same
            active_reminders.append(reminders[i]) #if it is, add to active reminders
            to_pop.append(i) 

    to_pop.sort()
    to_pop.reverse()

    if len(active_reminders) <= int(nums[0]): #
        await ctx.send("Error, number out of index of reminders")
        return
    else:
        string = "Deleted reminder"
        if(len(nums)>1):
            string+="s"
        string+=": "
        for num in to_pop:
            reminders.pop(num) #delete users reminds from all reminders
        for num in nums:
            active_reminders.pop(int(num)) #delete reminders not used
            string+=str(num)+" "
        reminders.pop(-1) #remove new line
        reminders += active_reminders + [''] #add users remaining reminders + new line

##    print(reminders)
    

    file = open('reminders.txt','w') #write new list, excluding sent reminders
    file.write('\n'.join(reminders))
    file.close()

    await ctx.send(string)

##    await re(ctx)

##used for the delete command     
async def re(ctx):
    author = ctx.author #get author
    try:
        guild = ctx.guild.id #get guild if there is one
    except:
        guild = None #no guild if its a DM
    channel = ctx.channel.id # get channel 
    
    file = open('reminders.txt','r')
    reminders = file.read().split('\n')#author id, reminder text, server id, channel id, time to send
    file.close()

    active_reminders = []
    
    for reminder in reminders:  #go through all reminders in file
        data = reminder.split(',') #get data
        if str(author.id) == data[0] and str(guild) == data[2] and str(channel) == data[3]:#make sure author, guild, and channel is the same
            active_reminders.append(reminder) #if it is, add to active reminders
    
            
    if len(active_reminders) >0: #if users have active reminders
        message = ''
        for i in range(len(active_reminders)): #itterate through and gather data
##            try:
                data = active_reminders[i].split(',')
                time = data[4] #datetime stored as yyyy-mm-dd hh:mm:ss.ssssss

                YMD = time.split(' ')[0].split('-') #year month and day

                HMS = time.split(' ')[1].split(':') # hour minute and seconds

                remind_time = datetime(int(YMD[0]),int(YMD[1]),int(YMD[2]),int(HMS[0]),int(HMS[1]),int(HMS[2].split('.')[0]))#make date time for reminder time

                time = str (remind_time - datetime.today())

                formatted_time = []

                if 'day' in time or 'days' in time:
                    formatted_time.append(time.split(',')[0]) # this gets the day
                    HMS = time.split(',')[1].split(':')
                else:
                    HMS = time.split(':')

                if int(HMS[0]) == 1: #make hours pretty (exclude 0 hours, singular one hour)
                    formatted_time +=['1','hour']
                elif int(HMS[0]) > 1:
                    formatted_time +=[HMS[0],'hours']

                if int(HMS[1]) == 1: #make minutes pretty (exclude 0 minutes, singular one minute)
                    formatted_time +=['1','minute']
                elif int(HMS[1]) > 1:
                    formatted_time +=[HMS[1],'minutes']

                if int(round(float(HMS[2]))) == 1: #make seconds pretty (exclude 0 seconds, singular one second)
                    formatted_time +=['1','second']
                elif int(round(float(HMS[2]))) > 1:
                    formatted_time +=[str(round(float(HMS[2]))),'seconds']

                
                    
                    
                
                message += '\n[' + str(i) + '] "'+ data[1] +'" in: ' + ' '.join(formatted_time) #add reminder to message
        await ctx.send(message) #send list of reminders with time remaining
    else:
        await ctx.send("No reminders found")
##            except:
##                print(reminder)
                
    
###runs every second, checks to see if any reminders need to be sent
###removes sent reminders from file
##should switch from polling to events
##thats a job for v3
@tasks.loop(seconds=1)  
async def send_messages():
    
    file = open('reminders.txt','r')
    reminders = file.read().split('\n')
    file.close()

    sent_reminders = []

    for i in range(len(reminders)):
        try:
            data = reminders[i].split(',') #author id, reminder text, server id, channel id, time to send, Days;Hours;Minutes;Seconds
            
            time = data[4] #datetime stored as yyyy-mm-dd hh:mm:ss.ssssss

            YMD = time.split(' ')[0].split('-') #year month and day

            HMS = time.split(' ')[1].split(':') # hour minute and seconds

            remind_time = datetime(int(YMD[0]),int(YMD[1]),int(YMD[2]),int(HMS[0]),int(HMS[1]),int(HMS[2].split('.')[0]))#make date time for reminder time

            if datetime.today() >= remind_time:  #compare to see if its time to remind
                formatted_time = [] #stores list of time values to send (36 minutes, 1 second)

                DHMS = data[5].split(';')

                if int(DHMS[0]) == 1: # make days pretty (exclude 0 days, add singular day)
                    formatted_time +=['1 day']
                elif int(DHMS[0]) > 1:
                    formatted_time +=[DHMS[0]+' days']

                if int(DHMS[1]) == 1:# make hours pretty (exclude 0 hours, add singular hour)
                    formatted_time +=['1 hour']
                elif int(DHMS[1]) > 1:
                    formatted_time +=[DHMS[1]+' hours']

                if int(DHMS[2]) == 1:# make minutes pretty (exclude 0 minutes, add singular minute)
                    formatted_time +=['1 minute']
                elif int(DHMS[2]) > 1:
                    formatted_time +=[DHMS[2]+' minutes']

                if int(round(float(DHMS[3]))) == 1:# make days seconds (exclude 0 seconds, add singular second)
                    formatted_time +=['1 second']
                elif int(round(float(DHMS[3]))) > 1:
                    formatted_time +=[str(round(float(DHMS[3])))+' seconds']

                time_ago = ', '.join(formatted_time) 
                
                if data[2] == 'None': #this means its in a DM
                    user = client.get_user(int(data[0]))

                    #following taken from Łukasz Kwieciński on https://stackoverflow.com/questions/66048484/discord-py-how-do-i-get-a-user-from-a-userid
                    if user is None: # Maybe the user isn't cached?
                        user = await client.fetch_user(id)
                    ##taken code end
                        
                    await user.send('<@!'+data[0]+'>'+' '+data[1] + ' (requested '+time_ago+ ' ago)')#send the reminder
                    sent_reminders.append(i) #mark reminder for deletion

                    
                else: #this means its in a server
                    for guild in client.guilds: #for every guild the bot is connected in
                        if guild.id == int(data[2]): #if the guild id matches
                            for channel in guild.channels: #look at all the channels in the guild
                                if channel.id == int(data[3]): #if the channel id matches
                                    sent_reminders.append(i) #mark reminder for deletion
                                    await channel.send('<@!'+data[0]+'>'+' '+data[1]+ ' (requested '+time_ago+ ' ago)') #send the reminder

        except:
            pass
##            print(reminders[i]) #usually just a new line

    sent_reminders.reverse() #to not mess up order (pop list end to start)
    for i in sent_reminders:
        reminders.pop(i) #delete reminders
    
    file = open('reminders.txt','w') #write new list, excluding sent reminders
    file.write('\n'.join(reminders))
    file.close()




send_messages.start() ##start the loop

async def rmp(ctx,arg):
    pass
    #take proffessor's name
    #output: rating, difficulty, retake%, top comment


##@client.command()
##async def help(ctx,*arg):
##    to_say = '```​gpa         syntax: !gpa <CLASS> ex: !gpa csci2021.\nhelp        Shows this message\nsetprefix   sets a custom prefix for the server syntax: !setprefix <PREFIX> ex: !setprefix $\n\nall data from:gophergrades.com and github.com/DannyG72/UMN-Grade-Dataset\nall ratings and difficulty gathered from rate my proffessor\n(if a prof\'s data/rating seems to be wrong @Errori#9025 on discord)```'
##    await ctx.send(to_say)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
