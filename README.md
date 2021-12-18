# gopher_grades_bot
the gopher grades bot for the umn, based off of the website: https://gophergrades.com/

## Attribution:
The idea for this bot came from gophergrades.com

all data from github.com/DannyG72/UMN-Grade-Dataset and ratemyprofessors.com

## code explination:
clean_me.py: turns the file from github into a clean csv file

gophergrades.py: takes a cleaned csv file and turns it into a data.eri file

rmp.py, scrapes rate my proffessor for all umn profs stored in bad_profs.txt

clean_profs.py: turns bad_profs into profs.txt, removes middle names and renames some profs

combiner.py: combines temp_data.eri and profs.txt into a final data.eri

MEGA_ERI_MAKER.py:combines the previous 5 files into one, good for new datasets/updating rmp

moen-nator.py: contains the gophergrades bot itself, needs data.eri and profs.txt file

## graph of functions:
```
dataset.xlsx->gopher_grades.py->temp_data.eri-----------+
							|
			                              	+-->combiner.py->data.eri->actual_bot.py
							|
rmp.py ->bad_profs.txt-->clean_profs.py->profs.txt------+
```



or


dataset.xlsx -> MEGA_ERI_MAKER -> data.eri-> moen-nator.py


the txt/eri created files are mainly backups/in progress version

data.eri is all that is needed for the bot to run

if you see a prof is on rmp but has no ratings edit the clean_profs.py dictionary and edit their name to whats in the temp_data.eri file

then run it and the combine.py file


## data.eri file:
structure
```
c:ABUS3051,845,33,3.6,4.00,2.50
i:Lori Bonderson,ABUS3051,102,5,-0.23,3.36
i:Monica Hamling,ABUS3051,54,2,0.03,3.63,4,3
i:Alyssa Maples,ABUS3051,178,7,-0.09,3.5,4,2
i:Carol Klempka,ABUS3051,366,14,0.05,3.65
i:Stacy O'Fallon,ABUS3051,31,1,0.17,3.77
i:Jeannine Kessler,ABUS3051,64,2,0.18,3.78
i:None,ABUS3051,50,2,0.16,3.76
c:ABUS3301,398,16,3.18,2.70,2.60
i:Scott Martens,ABUS3301,270,11,-0.01,3.16,2.7,2.6
i:Karen Schaffhausen,ABUS3301,128,5,0.05,3.23
c:ABUS4022W,709,27,3.44,4.90,1.70
i:Bradley Goodell,ABUS4022W,592,22,0.01,3.45,4.9,1.7
i:Brian Simons,ABUS4022W,117,5,-0.02,3.41
```

begins with c: this is a class


begins with i: this is an instructor



everything after : is data

```
c:class name, students, sections, gpa, avg rating, avg difficulty
i:prof name, class name, students, sections, gpa+/-, gpa, rating, difficulty
```

## FAQ:

why did you use .eri files?

because I wanted to use my initials


gophergrades.com has slightly different numbers, why is that?

slightly different rounding between versions, should only be off by .01 to .02 at most


why don't some proffessor's/classes don't appear/don't have ratings?

if a class is missing that means there wasn't enough data to have an avg gpa for the class

if a proffessor is missing that means they either weren't included in the csv file or not enough data to have an avg gpa

if a proffessor is missing ratings from rmp that means they either aren't on rmp or they have a different name on rmp

(I caught some but probably not all different names)


