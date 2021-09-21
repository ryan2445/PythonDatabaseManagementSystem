import os
import shutil

selectedDatabase = None

def createDatabase(databaseName):
    path = os.getcwd()

    path += '/' + databaseName

    if os.path.exists(path): return print("!Failed to create database", databaseName, "because it already exists.")

    os.mkdir(path)

    return print("Database", databaseName, "created.")

def dropDatabase(databaseName):
    global selectedDatabase

    path = os.getcwd()

    path += '/' + databaseName

    if not os.path.exists(path): return print("!Failed to delete database", databaseName, "because it does not exist")

    shutil.rmtree(path)

    if selectedDatabase == databaseName: selectedDatabase = None

    return print("Database", databaseName, "deleted.")

def useDatabase(databaseName):
    global selectedDatabase
    
    selectedDatabase = databaseName

    return print("Using database", selectedDatabase)

def createTable(commandArray):
    if not selectedDatabase: return print("No database selected.")

    tableName = commandArray[2]

    columns = ' '.join(commandArray[3 : len(commandArray)])

    columns = columns[1 : -1]

    columns = columns.split(',')

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    if os.path.exists(path): return print("!Failed to create table", tableName, "because it already exists.")

    file = open(path, 'w')

    line = ""

    for i in range(len(columns)):
        column = columns[i]

        if column[0] == " ": column = column[1 : ]

        line += column

        if not i == len(columns) - 1: line += " | "

    file.write(line)

    file.close()

    return print("Table", tableName, "created.")

def dropTable(tableName):
    if not selectedDatabase: return print("No database selected.")

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    if not os.path.exists(path): return print("!Failed to delete table", tableName, "because it does not exist.")

    os.remove(path)

    return print("Table", tableName, "deleted.")

def selectFromTable(commandArray):
    if commandArray[1] == "*": return selectAllFromTable(commandArray)

    return print("Unknown command.")

def selectAllFromTable(commandArray):
    if not selectedDatabase: return print("No database selected.")

    tableName = commandArray[-1]

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    if not os.path.exists(path): return print("!Failed to query table", tableName, "because it does not exist.")

    file = open(path, 'r')

    allLines = file.readlines()

    for line in allLines: print(line)

    return file.close()

def alterTable(commandArray):
    tableName = commandArray[2]

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    if not os.path.exists(path): return print("That table does not exist.")

    if commandArray[3] == "ADD": return alterTableAdd(tableName, path, commandArray[4 : len(commandArray)])

    return print("Invalid command.")

def alterTableAdd(tableName, path, column):
    column = ' '.join(column)

    addition = " | " + column

    file = open(path, 'a')

    file.write(addition)

    file.close()

    return print("Table", tableName, "modified.")

def CREATE(commandArray):
    if len(commandArray) < 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return createDatabase(commandArray[2])

    if len(commandArray) > 4 and commandArray[1] == 'TABLE': return createTable(commandArray)

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

def SELECT(commandArray):
    if len(commandArray) < 4: return print("Invalid command.")

    if "FROM" in commandArray: return selectFromTable(commandArray)

    return print("Invalid command.")

def ALTER(commandArray):
    if len(commandArray) < 6: return print("Invalid command.")

    if commandArray[1] == 'TABLE': return alterTable(commandArray)

def validateCommand(command):
    if command[-1] != ';': return False

    command = command.replace(';', '')

    commandArray = command.split()

    functionName = commandArray and commandArray[0]

    validFunctionName = functionName in ['CREATE', 'DROP', 'USE', 'SELECT', 'ALTER']

    if not validFunctionName: return False

    return commandArray

while True:
    command = input('--> ')

    if command == '.EXIT':
        print("All done.")
        break

    commandArray = validateCommand(command)

    if not commandArray:
        print("Invalid command.")
        continue

    globals()[commandArray[0]](commandArray)