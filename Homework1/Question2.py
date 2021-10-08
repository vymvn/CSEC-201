import os

def findPasswordTextFile():
    text_files = []
    for paths, dirs, files in os.walk("C:\\Users\\Ayman\\Dropbox\\Uni\\Year2_Fall\\CSEC-201\\CSEC201PyScripts"):
        for file in files:
            if file.endswith(".txt"):
                text_files.append(file)
                # print(file)
    for file in text_files:
        with open(file, "r") as f:
            print(f.read)





findPasswordTextFile()