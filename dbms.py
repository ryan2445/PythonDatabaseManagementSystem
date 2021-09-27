#   Ryan Hoffman
#   CS457 - Database Management Systems
#   9/27/2021

import os
import shutil
import sys

selectedDatabase = None

"""
createDatabase(databaseName)

- Constructs the path to the database by appending the name of the database to the current working directory
- Creates the database directory

"""
def createDatabase(databaseName):
    # Get current directory path
    path = os.getcwd()

    # Append database name in path
    path += '/' + databaseName

    # Check if path already exists
    if os.path.exists(path): return print("!Failed to create database", databaseName, "because it already exists.")

    # Make the directory
    os.mkdir(path)

    # Print confirmation
    return print("Database", databaseName, "created.")


"""
dropDatabase(databaseName)

- Constructs the path to the database by appending the name of the database to the current working directory
- Deletes the directory

"""
def dropDatabase(databaseName):
    # Get the global selectedDatabase variable
    global selectedDatabase

    # Get the current working directory
    path = os.getcwd()

    # Append database name to path
    path += '/' + databaseName

    # Check if the path exists
    if not os.path.exists(path): return print("!Failed to delete database", databaseName, "because it does not exist")

    # Delete the directory and all tables inside
    shutil.rmtree(path)

    # If the selectedDatabase is the database we just deleted, set the selectedDatabase to null
    if selectedDatabase == databaseName: selectedDatabase = None

    # Print confirmation
    return print("Database", databaseName, "deleted.")


"""
useDatabase(databaseName)

- Sets a global variable to store the name of the selected database

"""
def useDatabase(databaseName):
    global selectedDatabase
    
    selectedDatabase = databaseName

    return print("Using database", selectedDatabase)

"""
createTable(commandArray)

- Creates the file path to the table using the databaseName global variable and the table name
- Parses the column fields
- Writes the column fields to the text file
- Saves/closes the text file

"""
def createTable(commandArray):
    if not selectedDatabase: return print("No database selected.")

    tableName = commandArray[2]

    #   Re-joins the table parameters
    columns = ' '.join(commandArray[3 : len(commandArray)])

    #   Removes the first '(' and last ')' from the string
    columns = columns[1 : -1]

    #   Splits the string by comma, so each column and type is an element in the array
    columns = columns.split(',')

    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    if os.path.exists(path): return print("!Failed to create table", tableName, "because it already exists.")

    file = open(path, 'w')

    #   First line of the table's text file
    line = ""

    for i in range(len(columns)):
        #   Create a temp column variable
        column = columns[i]

        #   Remove the beginning space from the column if it exists
        if column[0] == " ": column = column[1 : ]

        #   Append the column to the line
        line += column

        #   If this is not the last element in the array, add a | to the string
        if not i == len(columns) - 1: line += " | "

    file.write(line)

    file.close()

    return print("Table", tableName, "created.")

""""
dropTable(tableName)

- Constructs the path to the table using the working directory, database name, and table name
- If the path exists, deletes the text file

"""
def dropTable(tableName):
    # Don't allow dropping tables without selecting a database
    if not selectedDatabase: return print("No database selected.")

    # Get the path of the table
    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    # If the table does not exist, return
    if not os.path.exists(path): return print("!Failed to delete table", tableName, "because it does not exist.")

    # Delete the table's text file
    os.remove(path)

    # Print confirmation
    return print("Table", tableName, "deleted.")

"""
selectFromTable(commandArray)

- Handles any command that begins with "SELECT"
- Calls appropriate function based on following arguments

"""
def selectFromTable(commandArray):
    if commandArray[1] == "*": return selectAllFromTable(commandArray)

    return print("Unknown command.")

"""
selectAllFromTable(commandArray)

- Called when command begins with "SELECT *"
- Calculates the path to the database using the current working directory, database name, and table name
- Reads each line form the text file and prints it to the terminal

"""
def selectAllFromTable(commandArray):
    # Don't allow selecting if no database selected
    if not selectedDatabase: return print("No database selected.")

    # Table name will be last command arg
    tableName = commandArray[-1]

    # Get the path of the table
    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    # If table doesn't exist, returh
    if not os.path.exists(path): return print("!Failed to query table", tableName, "because it does not exist.")

    # Open the table's text file
    file = open(path, 'r')

    # Read all lines from the file
    allLines = file.readlines()

    # Print each line
    for line in allLines: print(line)

    # Close the file
    return file.close()

"""
alterTable(commandArray)

- Ensures the path to the table exists
- Handles any commands related to altering a table

"""
def alterTable(commandArray):
    # Don't allow altering table with no database selected
    if not selectedDatabase: return print("No database selected.")

    # Get the table name
    tableName = commandArray[2]

    # Get the table's path
    path = os.getcwd() + '/' + selectedDatabase + '/' + tableName + '.txt'

    #   If table does not exist, return
    if not os.path.exists(path): return print("That table does not exist.")

    #   Call function to add fields to table
    if commandArray[3] == "ADD": return alterTableAdd(tableName, path, commandArray[4 : len(commandArray)])

    # Print confirmation
    return print("Invalid command.")

"""
alterTableAdd(tableName, path, column)

- Appends the column to the first line of the table's text file

"""
def alterTableAdd(tableName, path, column):
    # Re-join the column field (previously split by space with reset of command)
    column = ' '.join(column)

    # Create the string we will append to the first line in the text file
    addition = " | " + column

    # Open the text file
    file = open(path, 'a')

    # Write the line
    file.write(addition)

    # Close the file
    file.close()

    # Print confirmation
    return print("Table", tableName, "modified.")

"""
CREATE(commandArray)

- Handles commands that begin with "CREATE"
- Calls handling function for second argument (i.e. "DATABASE", "TABLE", etc.) 

"""
def CREATE(commandArray):
    if len(commandArray) < 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return createDatabase(commandArray[2])

    if len(commandArray) > 4 and commandArray[1] == 'TABLE': return createTable(commandArray)

    return print("Invalid command.")

"""
DROP(commandArray)

- Handles commands that begin with "DROP"
- Calls handling function for second argument (i.e. "DATABASE", "TABLE", etc.) 

"""
def DROP(commandArray):
    if len(commandArray) != 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return dropDatabase(commandArray[2])

    elif commandArray[1] == 'TABLE': return dropTable(commandArray[2])

    return print("Invalid command.")

"""
USE(commandArray)

- Handles commands that begin with "USE"
- Ensures that the database exists before calling useDatabase, which sets the global variable

"""
def USE(commandArray):
    if len(commandArray) != 2: return print("Invalid command.")
    
    if commandArray[1] not in os.listdir(): return print(commandArray[1], "is not a database.")

    return useDatabase(commandArray[1])

"""
SELECT(commandArray)

- Handles commands that begin with "SELECT"
- Calls handling function for third argument (i.e. "FROM" etc.) 

"""
def SELECT(commandArray):
    if len(commandArray) < 4: return print("Invalid command.")

    if "FROM" in commandArray: return selectFromTable(commandArray)

    return print("Invalid command.")

"""
ALTER(commandArray)

- Handles commands that begin with "ALTER"
- Calls handling function for second argument (i.e. "TABLE", etc.) 

"""
def ALTER(commandArray):
    if len(commandArray) < 6: return print("Invalid command.")

    if commandArray[1] == 'TABLE': return alterTable(commandArray)

"""
validateCommand(command)

- Does some generalized checking on the whole command to make sure it's valid before calling any other functions for the command

"""
def validateCommand(command):
    #   If the command does not end in ';', it's invalid
    if command[-1] != ';': return False

    #   Remove the ';' from the command
    command = command.replace(';', '')

    #   Split the command by spaces into an array
    commandArray = command.split()

    #   Get the first argument from the command
    functionName = commandArray and commandArray[0]

    #   Make sure the function name is in the list of valid function names
    validFunctionName = functionName in ['CREATE', 'DROP', 'USE', 'SELECT', 'ALTER']

    #   If not valid, return false
    if not validFunctionName: return False

    # If valid, return the command in its array form (split by spaces)
    return commandArray

"""
Main Code

- Loop to accept standard input commands
- Parses each command and calls appropriate handling function

"""
for command in sys.stdin:

    #   Removes any leading/trailing whitespace from the input
    command = command.strip()

    #   If command is blank or starts with '-', ignore and continue
    if not command or command[0] == '-':
        continue

    #   If command is .EXIT, break loop and end program
    if command == '.EXIT':
        print("All done.")
        break

    #   Validate the command, if valid, split into array by space, otherwise value will be false
    commandArray = validateCommand(command)

    #   If command is invalid, print and wait for next command
    if not commandArray:
        print("Invalid command.")
        continue

    #   Call the handling function for the first command arguement (i.e. CREATE calls CREATE function)
    globals()[commandArray[0]](commandArray)