
import os
from os import path

# Saves highest records to a text file
def SaveRecords(score,time):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(current_dir+"/records/records.txt", 'w') as f:
        f.write(str(score)+"\n")
        f.write(str(time))
    print("Records are recorded")

# Reads records from a text file
def ReadRecords():

    current_dir = os.path.dirname(os.path.realpath(__file__))
    if(path.exists(current_dir+"/records/records.txt")):
        file = open(current_dir+"/records/records.txt", "r")
        score = file.readline()
        time = file.readline()
    else:
        print("File doesn't exists so new one is created")
        SaveRecords(0,0)
        return 0,0
    if(score == "" or score == " " or time == "" or time == " "):
        print("Erorr")
        SaveRecords(0,0)
        return 0,0

    return eval(score),eval(time)

