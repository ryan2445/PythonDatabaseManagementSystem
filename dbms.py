import os

def createDatabase(databaseName):
    path = os.getcwd()

    path += '/' + databaseName

    try:
        os.mkdir(path)
    except:
        print("Database name already exists.")
        return

    print("Database", databaseName, "created.")

def dropDatabase(databaseName):
    path = os.getcwd()

    path += '/' + databaseName

    try:
        os.rmdir(path)
    except:
        print("Database does not exist.")
        return

    print("Database", databaseName, "deleted.")

def CREATE(commandArray):
    if commandArray[1] == 'DATABASE' and len(commandArray) == 3: createDatabase(commandArray[2])
    elif commandArray[1] == 'TABLE' and len(commandArray) == 3: print("put create table function here")
    else: print("Invalid command.")

def DROP(commandArray):
    if commandArray[1] == 'DATABASE' and len(commandArray) == 3: dropDatabase(commandArray[2])
    elif commandArray[1] == 'TABLE' and len(commandArray) == 3: print("put create table function here")
    else: print("Invalid command.")

command = None

while(command != ".EXIT"):
    command = input('--> ')

    commandArray = command.split()

    functionName = commandArray and commandArray[0]

    validFunctionName = functionName in ['CREATE', 'DROP', 'USE', 'SELECT', 'ALTER']

    if validFunctionName == False:
        print("Invalid command.")
        continue

    globals()[functionName](commandArray)