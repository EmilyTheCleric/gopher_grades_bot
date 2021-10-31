def combine():
    file = open("temp_data.eri",'r')
    eri = file.read()
    eri = eri.split("\n")
    file.close()
    ##print(eri)


    file = open("profs.txt",'r')
    profs = file.read()
    profs = profs.split("\n")
    file.close()
    ##print(profs)

    name_rate_diff = {}
    for line in profs:
        try:
            words = line.split(',')
            name = words[0].split(" ")
            name = name[0] + " " + name[1]
            name_rate_diff[name.lower()] = [words[1],words[2]]
        except:
            pass
##            print(line)
      

    same = {}

    count = 0
##    for line1 in eri:
##        word1=line1.split(",")
##        
##        for line2 in profs:
##            try:
##                
##                    
##                word2=line2.split(',')
##                names = word2[0].split(' ')#first *middle last
##                full_name_test =  names[0] +' '+ names[1] #full name
##        ##        print(full_name_test)
##        ##        print(word1[0])
##        ##        print(full_name_test in word1[0])
##                
##                if (names[0] in word1[0] and (names[1] in word1[0] or names[3] in word1[0])) and not full_name_test in word1[0]: # eric van wyk == eric wyk
##                    if"Kangjie Lu" in line:
##                        print("KANGJIE ERROR")
##                    same[line1] =line2
##            except:
##                try:
##                    if (names[0] in word1[0] and (names[1] in word1[0])) and not full_name_test in word1[0]: #chris kauffman == christopher kauffman
##                        if"Kangjie Lu" in line:
##                            print("KANGJIE ERROR")
##                        same[line1] =line2
##                except:
##                    pass
##        count += 1
##        if count %1000 == 0:
##            print(str(count)+"/"+str(len(eri))+' profs updated')

    vals = same.keys()
##    print(name_rate_diff["kangjie lu"])
##    print("i:Kangjie Lu,CSCI4061,263,10,0.22,3.52" in vals)
    string = ""
    for line in eri:    #go through data.eri
        if line in vals:#if it needs to be fixed, fix it
            values = same[line].split(",")
            string += line +',' + values[1]+","+values[2]+'\n'
        else:
            try:#otherwise, add rating and difficulty scores to instructors
                words = line.split(",")
                n = words[0].split(":")
                if n[0] == 'i':
                    name = n[1]
                    rate = name_rate_diff[name.lower()][0]
                    diff = name_rate_diff[name.lower()][1]
                    if"Kangjie Lu" in line:
                        print(rate,diff)
                    string += line +',' + rate+","+diff+'\n'
                else:
                    string += line +'\n'
            except:
    ##            print(line)
                string += line +'\n'

    file = open("data.eri","w")
    file.write(string)
    file.close()
##combine()

            
        
    
