import os
import zipfile

def findPasswordTextFile():
    """ Scans D drive for text files that could be a password lists and returns the passwords if found

    Returns:
        list: list of passwords
    """
    passwords = []
    text_files = []
    for root, dirs, files in os.walk("D:\\"):
        for file in files:
            if file.endswith(".txt"):
                text_files.append(os.path.join(root, file))

    for file in text_files:
        with open(file, "r") as f:
            file_contents = (f.readlines())
            for line in file_contents:
                if line.startswith("password_"):
                    password = line.split(":")
                    passwords.append(password[1].strip())
    return passwords

            
def crack_zip(world_list):
    """ Tries to extract the zip with the passwords from previous function

    Args:
        world_list (list): list of passwords to try
    """
    success = False
    myZip = "/Homework1/resources/encrypted.zip"
    with zipfile.ZipFile(myZip) as z:
        for password in world_list:
            try:
                z.extractall(pwd = bytes(password, 'utf-8'), path="/Homework1/resources/")
                success = True
            except:
                print("error occurred") 
    if success == True:
        print("Password was found file extracted successfully")
    else:
        print("No password found")


def main():
    crack_zip(findPasswordTextFile)


if __name__ == "__main__":
    main()