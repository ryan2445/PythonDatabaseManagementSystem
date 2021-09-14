import os
import shutil

selectedDatabase = None

def createDatabase(databaseName):
    path = os.getcwd()

    path += '/' + databaseName

    if os.path.exists(path): return print("Database", databaseName, "already exists")

    os.mkdir(path)

    return print("Database", databaseName, "created.")

def dropDatabase(databaseName):
    path = os.getcwd()

    path += '/' + databaseName

    if not os.path.exists(path): return print("Database", databaseName, "does not exist")

    shutil.rmtree(path)

    return print("Database", databaseName, "deleted.")

def useDatabase(databaseName):
    global selectedDatabase
    
    selectedDatabase = databaseName

    return print("Using database", selectedDatabase)

def createTable(tableName):
    if not selectedDatabase: return print("No database selected.")

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    file = open(path, 'w')

    file.close()

    return print("Created table", tableName)

def dropTable(tableName):
    if not selectedDatabase: return print("No database selected.")

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    if not os.path.exists(path): return print("Table", tableName, "does not exist.")

    os.remove(path)

    return print("Dropped table", tableName)

def CREATE(commandArray):
    if len(commandArray) != 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return createDatabase(commandArray[2])

    if commandArray[1] == 'TABLE': return createTable(commandArray[2])

    return print("Invalid command.")

def DROP(commandArray):
    if len(commandArray) != 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return dropDatabase(commandArray[2])

    elif commandArray[1] == 'TABLE': return dropTable(commandArray[2])

    return print("Invalid command.")

def USE(commandArray):
    if len(commandArray) != 2: return print("Invalid command.")
    
    if commandArray[1] not in os.listdir(): return print(commandArray[1], "is not a database.")

    return useDatabase(commandArray[1])

while True:
    command = input('--> ')

    if command == '.EXIT':
        print("All done.")
        break

    commandArray = command.split()

    functionName = commandArray and commandArray[0]

    validFunctionName = functionName in ['CREATE', 'DROP', 'USE', 'SELECT', 'ALTER']

    if validFunctionName == False:
        print("Invalid command.")
        continue

    globals()[functionName](commandArray)