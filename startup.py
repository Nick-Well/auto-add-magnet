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

start()

<<<<<<< HEAD

=======
>>>>>>> dc966cecc10a40570e3886b7c82e23e90c841e69

