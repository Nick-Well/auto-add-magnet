import glob
import requests
import re
from bs4 import BeautifulSoup
from transmission_rpc import Client


mountPoint = ""
shows = ""
movies = ""
docomentery = ""
folder = "/"

def get_data():
    global mountPoint
    global shows
    global movies
    global docomentery
    global folder
    with open("drive", "r") as f:
        info = f.readline().split()
    mountPoint = info[0]
    shows = info[1]
    movies = info[2]
    docomentery = info[3]
    lookForName()


#TODO:  it does this unneceserly wen the text file already has the latest
#       so need to check if its already incremented instead of re do it 
#       every time


def increment_episode(episode):
    print("incremented")
    season = episode[1:3]
    episode_num = int(episode[4:])
    episode_num += 1
    new_episode = f"s{season}e{episode_num:02d}"
    return new_episode


def clean_text(text):
    pattern = r'S\d{2}E\d{2}'
    cleaned_text = re.findall(pattern, text, re.IGNORECASE)
    return cleaned_text


def transmission(magnet, location):
    print("adding magnet to transmission")
    info = open("localInfo", "r")
    info = info.readline()
    info = info.split()
    c = Client(host = info[0], port = info[1], username=info[2], password=info[3])
    #print(info[0]+info[1])
    c.add_torrent(magnet, download_dir=location)


def lookForName():
    global mountPoint
    global shows
    global movies
    global docomentery
    global folder
    print("looking for names and incrementing")
    writeLines = []
    lastEp = "S00E00"
    with open("download.txt", "r") as f:
        for line in f:
            testWord = 0
            line = line.split()
            while testWord != 2:
                if testWord == 1:
                    name = line[1]
                    lineU = name[0].upper() + name[1:]
                    files = glob.glob(mountPoint + line[0] + "/**/*" + lineU +"*.mkv", recursive=True)
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
            writeLines.append(str(line[0] +" "+ line[1] +" "+ increment_episode(lastEp) +"\n").lower())
    with open("download.txt", "w") as w:
        w.writelines(writeLines)
    getMagnet()
            
            
def getMagnet():
    global mountPoint
    global shows
    global movies
    global docomentery
    global folder
    print("get magnet link")
    with open("download.txt", "r") as f:
        for line in f:
            name = line.split()
            #print(name[1])
            first = "https://www.magnetdl.org"
            URL = "https://www.magnetdl.org/"+ name[1][0] +"/" + name[1] +"-"+ name[2] +"-1080p-h264/se/desc/"
            #print(URL)
            with requests.Session() as session:
                session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
                page = requests.get(first)
                #print(page)
                response = session.get(URL, headers={"Accept" : "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.magnetdl.org", "Host": "www.magnetdl.org"})
                soup = BeautifulSoup(response.content, "lxml")
                link = soup.find('a',attrs={'href': re.compile("^magnet:/?.*"+name[1]+".*"+name[2], re.IGNORECASE)})
                if link:
                    print(link.get("href"))
                    transmission(link.get('href'), "/downloads"+name[0])



get_data()
