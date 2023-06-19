import requests
import glob
import re
from bs4 import BeautifulSoup

#TODO: Make a file with array: name (%00s %00e/complete) H264 %folder %DONE

#TODO: Check if file exist: error
#TODO: Check if name already exist on hardrive and add to the file if already exist
#TODO: imdb check epesods left too modify %DONE 
#TODO:      add date wen next epesode is out and skip if date doesnt match/biger  

#TODO: Look for the first magnet link. 
#TODO:      Add it to a file with distination folder
#TODO: Loop array: magnet %folder in to Transmission

#TODO: stages so no need to repeat it every time 
#TODO: 
#TODO: 

shows = "/tv"
docomentery = "/doc"
movies = "/movies"
folder = "/"

def clean_text(text):
    pattern = r'S\d{2}E\d{2}'
    cleaned_text = re.findall(pattern, text)
    return cleaned_text


def addName():
    name = input("add name: ") or 0
    if name == 0:
        print("needs a name")
    else:
        foldNr = int(input("folder 1.tv-shows 2.movies 3.docomentery: "))
        if foldNr == 1:
            folder = shows
        elif foldNr == 2:
            folder = movies
        elif foldNr == 3:
            folder == docomentery
        else:
            print("nofolder")
        downloadFile = open("download.txt", "a")
        downloadFile.write(folder + " " + name + "\n")
        downloadFile.close()


def lookForName():
    with open("download.txt", "r") as f:
        for line in f:
            line = line.split()
            print(line[0]+" "+line[1])
            oneStep = str("/mnt/HDD1" +line[0] + "/*" + line[1] +"*/*.mkv")
            inLocation = str("/mnt/HDD1" +line[0] + "/*" + line[1] +"*.mkv")
            
            filesF = glob.glob(oneStep)
            for file in filesF:
                print(clean_text(file))
            
            files = glob.glob(inLocation)
            for file in files:
                print(clean_text(file))

def getMagnet():
    with open("download.txt", "r") as f:
        for line in f:
            name = line.split()
            print(name[1])
            first = "https://www.magnetdl.org"
            URL = "https://www.magnetdl.org/s/" + name[1] + "-1080p-h264/se/desc/"

            with requests.Session() as session:
                session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
                page = requests.get(first)
                response = session.get(URL, headers={"Accept" : "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.magnetdl.org", "Host": "www.magnetdl.org"})
                soup = BeautifulSoup(response.content, "lxml")
                for link in soup.find_all('a',attrs={'href': re.compile("^magnet:/?.*"+name[1], re.IGNORECASE)}):
                    print(link.get('href'))
                    print(link)
while True:
    foldNr = input("1.getMagnet 2.lookForName 3.addName: ")
    if foldNr == "1":
        getMagnet()
    elif foldNr == "2":
        lookForName()
    elif foldNr == "3":
        addName()
    else:
        break




