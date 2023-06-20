import requests
import glob
import re
from transmission_rpc import Client
from bs4 import BeautifulSoup

#TODO: Make a file with array: name (%00s %00e/complete) H264 %folder %DONE

#TODO: Check if name already exist on hardrive and add to the file if already exist
#TODO: imdb check epesods left too modify %DONE 
#TODO:      add date wen next epesode is out and skip if date doesnt match/biger  

#TODO: Look for the first magnet link. 
#TODO:      Add it to a file with distination folder
#TODO: Loop array: magnet %folder in to Transmission

#TODO: stages so no need to repeat it every time 

#TODO: only open files ones and not for every call
#TODO: change the global veriables to classes
#TODO: folder information also to an array/ class object for easyer calls 
#TODO: 


shows = "/tv"
docomentery = "/doc"
movies = "/movies"
folder = "/"
mountPoint = "/mnt/HDD1"
    #print("defult: /transmission/")
    #webInterface = input ("webinterface: ")

def serverIp():
    ip = input("whats the ip of the Transmission server: ")
    print("defult: 9091")
    port = input("whats the port of the Transmission server: ") or 9091
    infoFile = open("localInfo", "a")
    infoFile.write(ip+" "+port)
    infoFile.close()


def clean_text(text):
    pattern = r'S\d{2}E\d{2}'
    cleaned_text = re.findall(pattern, text, re.IGNORECASE)
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


#TODO: split this up to 2 functions if not 3
def lookForName():
    writeLines = []
    with open("download.txt", "r") as f:
        lineNr = 0
        for line in f:
            testWord = 0
            lastEp = "S00E00"
            line = line.split()
            print(mountPoint + line[0]+" "+line[1])
            while testWord != 2:
                if testWord == 1:
                    name = line[1]
                    lineU = name[0].upper() + name[1:]
                    files = glob.glob(mountPoint + line[0] + "/**/*" + lineU +"*.mkv", recursive=True)
                    print(lineU)
                    for file in files:
                        text = clean_text(file)
                        if len(text) != 0:
                            if lastEp < text[0]:
                                lastEp = text[0]
                files = glob.glob(mountPoint + line[0] + "/**/*" + line[1] +"*.mkv", recursive=True)
                testWord+=1
                for file in files:
                    text = clean_text(file)
                    if len(text) != 0:
                        if lastEp < text[0]:
                            lastEp = text[0]
            print(lineNr)
            print(lastEp)
            writeLines.append(str(line[0] +" "+ line[1] +" "+ lastEp +"\n").lower())
            lineNr+=1
    with open("download.txt", "w") as w:
        w.writelines(writeLines)
            
            
def getMagnet():
    with open("download.txt", "r") as f:
        for line in f:
            name = line.split()
            print(name[1])
            first = "https://www.magnetdl.org"
            URL = "https://www.magnetdl.org/"+ name[1][0] +"/" + name[1] +"-"+ name[2] +"-1080p-h264/se/desc/"
            print(URL)
            with requests.Session() as session:
                session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
                page = requests.get(first)
                response = session.get(URL, headers={"Accept" : "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.magnetdl.org", "Host": "www.magnetdl.org"})
                soup = BeautifulSoup(response.content, "lxml")
                for link in soup.find_all('a',attrs={'href': re.compile("^magnet:/?.*"+name[1], re.IGNORECASE)}):
                    print(link.get('href'))

def start():
    while True:
        x = input("1.getMagnet 2.lookForName 3.addName 4.addTransmissionIp: ")
        if x == "1":
            getMagnet()
        elif x == "2":
            lookForName()
        elif x == "3":
            addName()
        elif x == "4":
            serverIp()
        else:
            break

start()


