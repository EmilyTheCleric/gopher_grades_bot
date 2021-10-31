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
dataset.csv->clean_me.py->gg.csv->gopher_grades.py->temp_data.eri--+

								   |

			                              	       	   +-->combiner.py->data.eri->moen-nator.py

								   |

rmp.py ->bad_profs.txt-->clean_profs.py->profs.txt-----------------+



or


dataset.csv -> MEGA_ERI_MAKER -> data.eri-> moen-nator.py


the txt/csv/eri files are mainly backups/in progress version

data.eri is all that is needed

if you see a prof is on rmp but has no ratings edit the clean_profs.py dictionary and edit their name to whats in the temp_data.eri file

then run it and the combine.py file


## data.eri file:
structure

c:ABUS3051,735,29,3.57

i:Lori Bonderson,ABUS3051,102,5,-0.2,3.36

i:Monica Hamling,ABUS3051,54,2,0.06,3.63,4,3

i:Alyssa Maples,ABUS3051,178,7,-0.06,3.5,4,2

i:Carol Klempka,ABUS3051,306,12,0.05,3.62

i:Stacy Ann Marr O'Fallon,ABUS3051,31,1,0.2,3.77

i:Jeannine Kessler,ABUS3051,64,2,0.21,3.78

c:ABUS3301,364,15,3.17

i:Scott Martens,ABUS3301,270,11,-0.0,3.16,2.7,2.6

i:Karen Schaffhausen,ABUS3301,94,4,0.02,3.19



begins with c: this is a class

begins with i: this is an instructor



everything after : is data

c:class name, students, sections, gpa

i:prof name, class name, students, sections, gpa+/-, gpa, rating, difficulty


## FAQ:

why did you use .eri files?

because I'm a narsicist and decided to use my initials as a powermove


gophergrades.com has slightly different numbers, why is that?

slightly different rounding between versions, should only be off by .01 to .02 at most


why don't some proffessor's/classes don't appear/don't have ratings?

if a class is missing that means there wasn't enough data to have an avg gpa for the class

if a proffessor is missing that means they either weren't included in the csv file or not enough data to have an avg gpa

if a proffessor is missing ratings from rmp that means they either aren't on rmp or they have a different name on rmp

(I caught some but probably not all different names)


## IMPROVEMENTS THAT CAN BE MADE:

better/faster web scraping

maybe use java/c to get online stuffs or selenium/scrapy

