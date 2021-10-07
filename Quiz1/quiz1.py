
import threading
import os

class readFileThread(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.info_file = file

    def run(self):
        with open(self.info_file, "r") as i:
            temp = i.readlines()
            files = []
            for file in temp:
                files.append(file.strip())
            files.sort()

            
            for dirpath, dirnames, filenames in os.walk("C:\\Users\\Ayman\\Dropbox\\Uni\\Year2_Fall\\CSEC-201\\CSEC201PyScripts"):
                filenames.sort()
                if filenames == files:
                    print("Found in: " + dirpath)



            # curr_dir = os.scandir()
            # for i in curr_dir:
            #     if i.is_dir():
            #         sub_dir_content = os.listdir(i.path)
            #         sub_dir_content.sort()
            #         if sub_dir_content == files:
            #             print(i.name)                    

testthread = readFileThread("Quiz1\Info.txt")
testthread.start()
