import requests
import glob
import re
from transmission_rpc import Client
from bs4 import BeautifulSoup


#TODO: imdb check epesods left too modify %DONE 
#TODO:      add date wen next epesode is out and skip if date doesnt match/biger  

#TODO: change the global veriables to classes
#TODO: folder information also to an array/ class object for easyer calls 
#TODO: 


def start():
    while True:
        x = input("1.addName 2.addTransmissionIp: ")
        if x == "1":
            addName()
        elif x == "2":
            serverIp()
        else:
            break


def clean_text(text):
    pattern = r'S\d{2}E\d{2}'
    cleaned_text = re.findall(pattern, text, re.IGNORECASE)
    return cleaned_text

#1
#def increment_episode(episode):
#    season = episode[1:3]
#    episode_num = int(episode[4:])
#    episode_num += 1
#    new_episode = f"s{season}e{episode_num:02d}"
#    return new_episode
#
#
#def transmission(magnet, location):
#    info = open("localInfo", "r")
#    info = info.readline()
#    info = info.split()
#    c = Client(host = info[0], port = info[1], username=info[2], password=info[3])
#    print(info[0]+info[1])
#    c.add_torrent(magnet, download_dir=location)
#1

shows = "/tv"
docomentery = "/doc"
movies = "/movies"
folder = "/"
mountPoint = "/mnt/HDD1"
def driveLocation():
    info = []
    info.append(input("the mount point: "))
    info.append(input("tv-shows end point: "))
    info.append(input("movies end point: "))
    info.append(input("docomentery end point: "))
    drive = open("drive", "a")
    for data in info:
        drive.write(data + " ")
    drive.close
    

#TODO: change varibles to array
def serverIp():
    ip = input("whats the ip of the Transmission server: ")
    print("defult: 9091")
    port = str(input("whats the port of the Transmission server: ") or 9091)
    print("defult: transmission")
    usern = input("whats the username of the Transmission server: ") or "transmission"
    print("defult: password")
    passwd = input("whats the password of the Transmission server: ") or "password"
    infoFile = open("localInfo", "w")
    infoFile.write(ip+" "+port+" "+usern+" "+passwd)
    infoFile.close()


def addName():
    while True:
        name = input("add name: ") or 0
        if name == 0:
            print("needs a name")
            break
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
        print("defult: yes")
        breakIf = input("do you whant to add more: Yes/no ") or "yes"
        if breakIf != "yes":
            lookForName()
            break
#2
#TODO: split this up to 2 functions if not 3
#def lookForName():
#    writeLines = []
#    with open("download.txt", "r") as f:
#        lineNr = 0
#        for line in f:
#            testWord = 0
#            lastEp = "S00E00"
#            line = line.split()
#            
#            while testWord != 2:
#                if testWord == 1:
#                    name = line[1]
#                    lineU = name[0].upper() + name[1:]
#                    files = glob.glob(mountPoint + line[0] + "/**/*" + lineU +"*.mkv", recursive=True)
#                    for file in files:
#                        text = clean_text(file)
#                        if len(text) != 0:
#                            if lastEp < text[0]:
#                                lastEp = text[0]
#                files = glob.glob(mountPoint + line[0] + "/**/*" + line[1] +"*.mkv", recursive=True)
#                testWord+=1
#                for file in files:
#                    text = clean_text(file)
#                    if len(text) != 0:
#                        if lastEp < text[0]:
#                            lastEp = text[0]
#            writeLines.append(str(line[0] +" "+ line[1] +" "+ increment_episode(lastEp) +"\n").lower())
#            lineNr+=1
#    with open("download.txt", "w") as w:
#        w.writelines(writeLines)
#            
#            
#def getMagnet():
#    with open("download.txt", "r") as f:
#        for line in f:
#            name = line.split()
#            print(name[1])
#            first = "https://www.magnetdl.org"
#            URL = "https://www.magnetdl.org/"+ name[1][0] +"/" + name[1] +"-"+ name[2] +"-1080p-h264/se/desc/"
#            print(URL)
#            with requests.Session() as session:
#                session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
#                page = requests.get(first)
#                response = session.get(URL, headers={"Accept" : "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.magnetdl.org", "Host": "www.magnetdl.org"})
#                soup = BeautifulSoup(response.content, "lxml")
#                link = soup.find('a',attrs={'href': re.compile("^magnet:/?.*"+name[1]+".*"+name[2], re.IGNORECASE)})
#                if link:
#                    transmission(link.get('href'), name[0])
#2

#driveLocation()
start()



