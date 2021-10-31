from bs4 import BeautifulSoup, SoupStrainer
import requests
import lxml
import time

class Prof:
    def __init__(self, name, rating, difficulty):
        self.name = name
        self.rating = rating
        self.difficulty = difficulty
    def __str__(self):
        return self.name + "," +self.rating+","+self.difficulty+"\n"
    
profs = []
prof_links = []
base_url = "https://www.ratemyprofessors.com"

##file = open("links.txt","r")
##lines = file.read()
##file.close()
##lines = lines.split("\n")
##for line in lines:
##    prof_links.append(line)

only_text = SoupStrainer("div")
only_a = SoupStrainer("li")
def get():
    
    for i in range(273): #get all the links
        #url to page of all umn profs
        url = "https://www.ratemyprofessors.com/search.jsp?query=&queryoption=HEADER&stateselect=&country=&dept=&queryBy=teacherName&facetSearch=true&schoolName=university+of+minnesota+%5C%5C-+twin+cities&offset="+str(i*20)+"&max=20"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    ##    print("Soupified")
    ##    print('len = ' +str(len(soup.find_all('li', class_ = 'listing PROFESSOR'))))
        for item in soup.find_all('li', class_ = 'listing PROFESSOR'):                      #get all links
            links_with_text = [a['href'] for a in soup.find_all('a', href=True) if a.text]  #get all links
            for l in links_with_text:
                if "ShowRatings.jsp" in l:
                    prof_links.append(l)

##        print(i)
    good_links = []
    for link in prof_links:
        if not link in good_links:
            good_links.append(link) #some links are in there twice, gotta prune it so it runs in a reasonable amount of time
   

    print(str(len(good_links)) + ' links found')
                    
    for link in good_links:             #for every prof
        url = base_url+link             #the url 
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        rating = soup.find('div', class_ = 'RatingValue__Numerator-qw8sqy-2 liyUjw').getText() #get rating/5
        name = soup.find('div', class_ ="NameTitle__Name-dowf0z-0 cfjPUG").getText()           #get name of prof
        difficulty = "0"
        for i in soup.find_all("div",class_="FeedbackItem__FeedbackNumber-uof32n-1 kkESWs"):   #% and difficulty same class, gotta do this to get the real difficulty
            t = i.getText()
            if "%" in t:
                pass
            else:
                difficulty=t
                
            
        prof = Prof(name,rating,difficulty)   #make prof class
        profs.append(prof)  
        if len(profs) % 150 == 0:       #give incremental updates
            print(str(len(profs))+'/'+str(len(good_links))+' proffessors downloaded')

def write():
    get()
    string = ""
    for p in profs:   #write all profs, ratings, and difficulties
        string += p.__str__()
        
    file = open("bad_profs.txt","w")
    file.write(string)
    file.close()
    
start_time = time.time()
print("unstrained")
get()
print("--- %s seconds ---" % (time.time() - start_time))
input('quit')
##print(profs[0])
        






