change = {"Chris Kauffman":"Christopher Kauffman", "Kuen-Bang": "F." ,"Jim Parker":"James Parker",
          "Jensen Kathryn":"Kathryn Jensen"} #dict of all names that need to be changed
def clean():
    with open("bad_profs.txt") as file:
        lines = [line for line in file]
    new_words = []
    for line in lines:                          #for every line
        words = line.split(',')
        name = words[0].split(' ')
        try:
            if len(name) == 4: #if they have a middle name listed
                try:
                    fname = change[name[0]] + ' ' + name[2] #check if first name is in dic
                except:
                    try:
                        fname = change[name[0] + ' ' + name[2]] #check if last name is in dic
                    except:
                        fname = name[0] + ' ' + name[2]#not in dic
                    
                        
            else:
                try:
                    fname = change[name[0]] + ' ' + name[1]#check if first name is in dic
                except:
                    try:
                        fname = change[name[0] + ' ' + name[1]]#check if last name is in dic
                    except:
                        fname = name[0] + ' ' + name[1]#not in dic
                    
        except:
            print(line)
        words[0] = fname #set name as to what was calculated before
        nl = ','.join(words)
        new_words.append(nl)
    new_words = '\n'.join(new_words)

    file = open("profs.txt",'w') #write to new, better, and sexier file ;)
    file.write(new_words)
    file.close()
    
