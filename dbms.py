#   Ryan Hoffman
#   CS457 - Database Management Systems
#   9/27/2021

import os
import shutil
import sys

selectedDatabase = None
terminal = ""

"""
"""
def getPath(databaseName, tableName = None):
    path = os.getcwd() + '/' + databaseName.lower()

    if tableName: path += '/' + tableName.lower() + '.txt'

    return path

"""
createDatabase(databaseName)

- Constructs the path to the database by appending the name of the database to the current working directory
- Creates the database directory

"""
def createDatabase(databaseName):
    # Get current directory path
    path = getPath(databaseName)

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
    path = getPath(databaseName)

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

    #   Get the path to the table's text file
    path = getPath(selectedDatabase, tableName)

    #   If the path does not exist, return
    if os.path.exists(path): return print("!Failed to create table", tableName, "because it already exists.")

    #   Open the text file
    file = open(path, 'w')

    #   Remove trailing/leading whitespace from the columns
    for i in range(len(columns)): columns[i] = columns[i].strip()

    #   Create the line to write to the text file
    line = ' | '.join(columns)

    #   Write the line
    file.write(line + "\n")

    #   Close the file
    file.close()

    #   Return confirmation
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
    path = getPath(selectedDatabase, tableName)

    # If the table does not exist, return
    if not os.path.exists(path): return print("!Failed to delete table", tableName, "because it does not exist.")

    # Delete the table's text file
    os.remove(path)

    # Print confirmation
    return print("Table", tableName, "deleted.")

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
    path = getPath(selectedDatabase, tableName)

    # If table doesn't exist, returh
    if not os.path.exists(path): return print("!Failed to query table", tableName, "because it does not exist.")

    # Open the table's text file
    file = open(path, 'r')

    # Read all lines from the file
    allLines = file.readlines()

    # Print each line
    for line in allLines: print(line.strip())

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
    path = getPath(selectedDatabase, tableName)

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
    file = open(path, 'r')

    #   Read all the lines from the file
    lines = file.readlines()

    #   Close the file
    file.close()

    #   Remove the trailing \n from the line
    lines[0] = lines[0].replace("\n", "")

    #   Append the addition
    lines[0] += addition

    #   Open the file again in write mode this time
    file = open(path, 'w')

    #   Write the lines back to the file
    file.writelines(lines)

    # Close the file
    file.close()

    # Print confirmation
    return print("Table", tableName, "modified.")

"""
insertInto(tableName, params)


"""
def insertInto(tableName, params):
    # Get the table's path
    path = getPath(selectedDatabase, tableName)

    # If table does not exist, return
    if not os.path.exists(path): return print("That table does not exist.")

    #   Re-join params that were previously split by space
    params = ' '.join(params)

    #   Remove 'values(' from beginning of string and ')' from end of string
    params = params[7 : len(params) - 1]

    #   Split by comma to get each param individually
    params = params.split(',')

    #   Remove trailing/leading whitespace and any apostrophe characters
    for i in range(len(params)): params[i] = params[i].strip().replace('\'', '')

    #   Open the file in append mode
    file = open(path, 'a')

    #   Re-join parameters
    line = ' | '.join(params)

    #   Write the line
    file.write(line + "\n")

    #   Close the text file
    file.close()

    #   Return confirmation
    return print("1 new record inserted.")

"""
create(commandArray)

- Handles commands that begin with "create"
- Calls handling function for second argument (i.e. "DATABASE", "TABLE", etc.) 

"""
def create(commandArray):
    if len(commandArray) < 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return createDatabase(commandArray[2])

    if len(commandArray) > 4 and commandArray[1] == 'TABLE': return createTable(commandArray)

    return print("Invalid command.")

"""
drop(commandArray)

- Handles commands that begin with "drop"
- Calls handling function for second argument (i.e. "DATABASE", "TABLE", etc.) 

"""
def drop(commandArray):
    if len(commandArray) != 3: return print("Invalid command.")

    if commandArray[1] == 'DATABASE': return dropDatabase(commandArray[2])

    elif commandArray[1] == 'TABLE': return dropTable(commandArray[2])

    return print("Invalid command.")

"""
use(commandArray)

- Handles commands that begin with "use"
- Ensures that the database exists before calling useDatabase, which sets the global variable

"""
def use(commandArray):
    if len(commandArray) != 2: return print("Invalid command.")
    
    if commandArray[1].lower() not in os.listdir(): return print(commandArray[1], "is not a database.")

    return useDatabase(commandArray[1])

"""
select(commandArray)

- Handles commands that begin with "select"
- Calls handling function for third argument (i.e. "FROM" etc.) 

"""
def select(commandArray):
    if not selectedDatabase: return print("No database selected.")

    if len(commandArray) < 4: return print("Invalid command.")

    if commandArray[1] == "*": return selectAllFromTable(commandArray)

    fromIndex = commandArray.index("from")

    selectedCols = commandArray[1 : fromIndex]

    selectedColsIndexes = []

    for i in range(len(selectedCols)): selectedCols[i] = selectedCols[i].replace(',', '').strip()

    tableName = commandArray[fromIndex + 1]

    path = getPath(selectedDatabase, tableName)

    if not os.path.exists(path): return print("That database or table name does not exist.")

    file = open(path)

    lines = file.readlines()

    file.close()

    #   Split first row (the row containing column names) by ' | '
    headers = lines[0].split(' | ')

    for i in range(len(headers)):
        for j in range(len(selectedCols)):
            if selectedCols[j] in headers[i]: selectedColsIndexes.append(i)

    whereIndex = commandArray.index("where")

    #   This is the column name of the 'where' clause
    whereCol = commandArray[whereIndex + 1]

    #   Conditon operator in the where statement
    whereColCond = commandArray[whereIndex + 2]

    #   This is the value of the column name in the 'where' clause
    whereColVal = commandArray[whereIndex + 3].replace('\'', '')

    #   This is the index of the column name in the 'where' clause
    whereColIndex = None

    whereColType = None

    #   Find the index of the column name from the 'where' clause in the first row
    for i in range(len(headers)):
        if whereCol in headers[i]:
            whereColIndex = i
            whereColType = headers[i].split()[1]
            break
    
    #   Iterate through each row
    for i in range(len(lines)):
        #   Split the row by columns
        lineArray = lines[i].split(' | ')

        shouldPrint = i == 0 or evalCond(lineArray[whereColIndex], whereColCond, whereColVal, whereColType)

        if not shouldPrint: continue

        toPrint = []

        for i in range(len(selectedColsIndexes)):
            toPrint.append(lineArray[selectedColsIndexes[i]].strip())

        print(' | '.join(toPrint))

"""
alter(commandArray)

- Handles commands that begin with "alter"
- Calls handling function for second argument (i.e. "TABLE", etc.) 

"""
def alter(commandArray):
    if len(commandArray) < 6: return print("Invalid command.")

    if commandArray[1] == 'TABLE': return alterTable(commandArray)

"""
insert(commandArray)



"""
def insert(commandArray):
    # Don't allow inserting in table with no database selected
    if not selectedDatabase: return print("No database selected.")

    if len(commandArray) < 4: return print("Invalid command")

    if commandArray[1] == 'into': return insertInto(commandArray[2], commandArray[3 : len(commandArray)])

"""
update(commandArray)



"""
def update(commandArray):
    #   If no selected database, return
    if not selectedDatabase: return print("No database selected.")

    #   If command is no proper length, return
    if len(commandArray) < 6: return print("Invalid command")

    #   Get the table name
    tableName = commandArray[1]

    #   Get the path to the table's text file inside the database directory
    path = getPath(selectedDatabase, tableName)

    #   If the path does not exist, return
    if not os.path.exists(path): return print("That table does not exist.")

    #   Open the table's text file in read mode
    file = open(path, 'r')

    #   Read all lines from the text file into an array
    lines = file.readlines()

    #   Close the file
    file.close()

    #   Split first row (the row containing column names) by ' | '
    headers = lines[0].split(' | ')

    #   This is the name of the column we're setting
    setCol = commandArray[3]

    #   This is the index of the column in the array of columns for each row
    setColIndex = None

    #   This is the value we are setting the column to
    setColVal = commandArray[5].replace('\'', '')

    #   Find the index of the column name in the array of columns from the first row
    for i in range(len(headers)):
        if setCol in headers[i]:
            setColIndex = i
            break

    #   This is the column name of the 'where' clause
    whereCol = commandArray[7]

    #   This is the index of the column name in the 'where' clause
    whereColIndex = None

    #   This is the value of the column name in the 'where' clause
    whereColVal = commandArray[9].replace('\'', '')

    #   Find the index of the column name from the 'where' clause in the first row
    for i in range(len(headers)):
        if whereCol in headers[i]:
            whereColIndex = i
            break

    #   Init a counter to count how many rows we update
    recordsModified = 0
    
    #   Iterate through each row
    for i in range(len(lines)):
        #   Skip the first line (contains column names / types)
        if i == 0: continue

        #   Split the row by columns
        lineArray = lines[i].split(' | ')

        #   Check if the row needs an update
        needsUpdate = lineArray[whereColIndex] = whereColVal

        #   If the row needs an update
        if needsUpdate:
            #   Get the column value that needs to be replaced
            toReplace = lineArray[setColIndex]

            #   Replace the value in the row and set the row again
            lines[i] = lines[i].replace(toReplace, setColVal)

            #   Add a new line to the end if it doesn't have one
            if lines[i][-1] != "\n": lines[i] += "\n"

            #   Increment recordsModified
            recordsModified += 1
    
    #   Open the same text file, except in write mode this time
    file = open(path, 'w')

    #   Write the lines back into the text file
    file.writelines(lines)

    #   Close the text file
    file.close()

    #   Print confirmation
    confirmation = str(recordsModified) + ' record' + ('s' if recordsModified != 1 else '') + ' modified.'
    return print(confirmation)

def evalCond(left, operator, right, type = 'str'):
    if type == 'int':
        left = int(left)
        right = int(right)
    elif type == 'float':
        left = float(left)
        right = float(right)

    if operator == '=': return left == right
    elif operator == '<': return left < right
    elif operator == '>': return left > right
    elif operator == '!=': return left != right

"""
delete(commandArray)



"""
def delete(commandArray):
    #   If no selected database, return
    if not selectedDatabase: return print("No database selected.")

    #   If command is no proper length, return
    if len(commandArray) < 6: return print("Invalid command")

    #   Get the table name
    tableName = commandArray[2]

    #   Get the path to the table's text file inside the database directory
    path = getPath(selectedDatabase, tableName)

    #   If the path does not exist, return
    if not os.path.exists(path): return print("That table does not exist.")

    #   Open the table's text file in read mode
    file = open(path, 'r')

    #   Read all lines from the text file into an array
    lines = file.readlines()

    #   Close the file
    file.close()

    #   Split first row (the row containing column names) by ' | '
    headers = lines[0].split(' | ')
    
    whereColType = None

    #   This is the column name of the 'where' clause
    whereCol = commandArray[4]

    #   This is the index of the column name in the 'where' clause
    whereColIndex = None

    whereColCond = commandArray[5]

    #   This is the value of the column name in the 'where' clause
    whereColVal = commandArray[6].replace('\'', '')

    #   Find the index of the column name from the 'where' clause in the first row
    for i in range(len(headers)):
        if whereCol in headers[i]:
            whereColIndex = i
            whereColType = headers[i].split()[1]
            break
    
    #   Init a counter to count how many rows we update
    recordsModified = 0

    toRemove = []
    
    #   Iterate through each row
    for i in range(len(lines)):
        if i == 0: continue

        #   Split the row by columns
        lineArray = lines[i].split(' | ')

        #   Check if the row needs an update
        needsUpdate = evalCond(lineArray[whereColIndex], whereColCond, whereColVal, whereColType)

        #   If the row needs an update
        if needsUpdate:
            toRemove.append(lines[i])

            #   Increment recordsModified
            recordsModified += 1
        
    for row in toRemove: lines.remove(row)
        
    #   Open the same text file, except in write mode this time
    file = open(path, 'w')

    #   Write the lines back into the text file
    file.writelines(lines)

    #   Close the text file
    file.close()
    
    confirmation = str(recordsModified) + ' record' + ('s' if recordsModified != 1 else '') + ' modified.'
    return print(confirmation)

"""
validateCommand(command)

- Does some generalized checking on the whole command to make sure it's valid before calling any other functions for the command

"""
def validateCommand(command):
    #   Remove the ';' from the command
    command = command.replace(';', '')

    #   Split the command by spaces into an array
    commandArray = command.split()

    #   Get the first argument from the command
    functionName = commandArray and commandArray[0]

    #   Make function name lowercase
    functionName = functionName.lower()

    #   Set lower-case version of function name back in commandArray
    commandArray[0] = functionName

    #   Make sure the function name is in the list of valid function names
    validFunctionName = functionName in ['create', 'drop', 'use', 'select', 'alter', 'insert', 'update', 'delete']

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
    terminal += command.strip()

    #   If no commnand value, continue
    if not terminal: continue

    #   If command is blank or starts with '-', reset the terminal input and continue
    if terminal[0] == '-':
        terminal = ""
        continue

    #   If command is .EXIT, break loop and end program
    if terminal == '.EXIT':
        print("All done.")
        break


    #   If terminal doesn't start with ; and doesn't end in a space, add one and continue
    if terminal[-1] != ";":
        if terminal[-1] != " ": terminal += " "
        continue

    #   Validate the command, if valid, split into array by space, otherwise value will be false
    commandArray = validateCommand(terminal)

    #   Reset terminal input after command is entered
    terminal = ""

    #   If command is invalid, print and wait for next command
    if not commandArray:
        print("Invalid command.")
        continue

    #   Call the handling function for the first command arguement (i.e. CREATE calls CREATE function)
    globals()[commandArray[0]](commandArray)