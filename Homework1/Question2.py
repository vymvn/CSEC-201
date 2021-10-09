import os
import zipfile
import threading
import time




def findPasswordTextFile():
    """ Scans C drive for text files that could be a password lists and returns the passwords if found

    Returns:
        list: list of passwords
    """
    count = 0
    passwords = []
    text_files = []
    myPath = "C:\\"
    for root, dirs, files in os.walk(myPath):

        for file in files:
            if file.endswith(".txt"):
                text_files.append(os.path.join(root, file))
    for file in text_files:
        count += 1
        printProgressBar(count, len(text_files), prefix="Looking for passwords....")
        try:
            with open(file, "r") as f:
                try:
                    file_contents = (f.readlines())
                except:
                    pass
                for line in file_contents:
                    if line.startswith("password_"):
                        password = line.split(":")
                        passwords.append(password[1].strip())
        except:
            pass
    return passwords

            
def crack_zip(world_list):
    """ Tries to extract the zip with the passwords from previous function

    Args:
        world_list (list): list of passwords to try
    """
    success = False
    myZip = "Homework1\\resources\\encrypted.zip"
    with zipfile.ZipFile(myZip) as z:
        for password in world_list:
            try:
                z.extractall(pwd=bytes(password, 'utf-8'), path="Homework1\\resources")
                success = True
            except:
                pass
    if success == True:
        print("Password was found file extracted successfully")
    else:
        print("No password found")


def animate():
    while done == False:
        print('\rScanning drive |', end="")
        time.sleep(0.1)
        print('\rScanning drive /', end="")
        time.sleep(0.1)
        print('\rScanning drive -', end="")
        time.sleep(0.1)
        print('\rScanning drive \\', end="")
        time.sleep(0.1)
    print('\rDone!     ', end="")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print("\n")


def main():
    global done
    done = False
    animate()
    password_list = findPasswordTextFile()
    done = True
    crack_zip(password_list)

if __name__ == "__main__":
    main()
    input()