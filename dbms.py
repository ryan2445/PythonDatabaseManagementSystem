#   Ryan Hoffman - 8001139126
#   CS457 - Database Management Systems
#   11/29/2021

import os
import shutil
import sys
import uuid

selectedDatabase = None
terminal = ""

transactionId = None
transactions = {}

"""
begin(commandArray)

-   Function used to begin a transaction
-   Sets a unique id for the process to operate under
"""
def begin(commandArray):
    #   Get the process' transaction id global variable
    global transactionId
    
    #   Set the process' trasaction id global variable
    transactionId = str(uuid.uuid4())

    #   Print the confirmation
    return print("Transaction starts.")

"""
commit(commandArray)

-   Function used to commit transactions
-   Deletes the old file before the transaction and renames the new file
    with the updated data to the old file's name
"""
def commit(commandArray):
    #   Get global transaction variables
    global transactionId
    global transactions

    #   If there are no transactions to commit, do nothing
    if len(transactions) == 0:
        return print("Transaction abort.")

    #   Handle each transaction
    for oldPath, newPath in transactions.items():
        #   Remove the old file before the transaction
        os.remove(oldPath)

        #   Rename the file with the updated data to the old file's name
        os.rename(newPath, oldPath)

    #   Open the locked tables file
    lockedTablesFile = open(os.getcwd() + "/lockedTables.txt", "r")

    #   Get all the locked tables
    lockedTables = lockedTablesFile.readlines()

    #   Create an array of tables to unlock
    toRemove = []

    #   Iterate through transaction
    for oldPath, newPath in transactions.items():
        #   If the transaction table is in the locked tables
        if os.path.basename(oldPath)[ : -4] in lockedTables:
            #   Add the table to the array of tables to be unlocked
            toRemove.append(os.path.basename(oldPath)[ : -4])

    #   Iterate through all tables to be unlocked
    for table in toRemove:
        #   Remove the table from the locked array
        lockedTables.remove(table)
    
    #   Open the locked tables file again in write mode
    lockedTablesFile = open(os.getcwd() + "/lockedTables.txt", "w")

    #   Write the updated list of locked tables to the file
    lockedTablesFile.writelines(lockedTables)

    #   Close the locked tables file
    lockedTablesFile.close()

    #   Reset the transaction id and transactions dictionary
    transactionId = None
    transactions = {}

    #   Print transaction commit confirmation
    return print("Transaction committed.")

"""
getPath(databaseName, tableName)

-   Returns a path to the specified database or table

"""
def getPath(databaseName, tableName = None):
    #   Get the path by combining the current workign directory with the database name
    path = os.getcwd() + '/' + databaseName.lower()

    #   If a table name is specified, append table to name to path
    if tableName: path += '/' + tableName.lower() + '.txt'

    #   Return the path
    return path

def tableLocked(tableName):
    path = os.getcwd() + "/lockedTables.txt"

    if not os.path.exists(path):
        file = open(path, "w")

        file.close()

    file = open(path, "r")

    tables = file.readlines()

    for table in tables:
        if tableName == table:
            return True

    tables.append(tableName)

    file = open(path, "w")

    file.writelines(tables)

    file.close()
    
    return False

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

    #   Re-join the command
    commandArray = " ".join(commandArray)

    #   Find the index of the first parenthesis
    parenIndex = commandArray.index("(")

    #   Add a space between the parenthesis and the table name
    if commandArray[parenIndex - 1] != " ":
        commandArray = commandArray[:parenIndex] + " " + commandArray[parenIndex:]

    #   Re-split the command and proceed with normal handling
    commandArray = commandArray.split(" ")

    #   Get the name of the table
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
countFromTable(commandArray)

-   Returns the number of rows for a given table

"""
def countFromTable(commandArray):
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

    #   Close the file
    file.close()

    #   The number of items is the amount of lines from the table minus 1 for the column headers
    return print("COUNT(*)\n" + str(len(allLines) - 1))

"""
avgFromTable(commandArray)

-   Returns the average value of a given column for a given table (assuming integers or floats)

"""
def avgFromTable(commandArray):
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

    #   Close the file
    file.close()

    #   Find the column from the table that we are getting the average of
    column = commandArray[1][4 : -1]

    #   Pull the headers from the table
    headers = allLines[0]

    #   Split the headers into an array
    headers = headers.split(" | ")

    #   Initialize an index for the index of the column from the command input
    colIndex = -1

    #   Go through each header, find the index of the column from the command input
    for i in range(len(headers)):
        if headers[i].startswith(column): colIndex = i

    #   Initialize a sum variable for the sum of all column values
    sum = 0
    
    #   Iterate through each line, adding the column value to the sum
    for i in range(len(allLines)):
        if i == 0: continue

        line = allLines[i]

        line = line.split(" | ")

        sum += float(line[colIndex])

    #   Divide the sum by the number of values we added together to get the average
    average = sum / (len(allLines) - 1)

    #   Print the average
    return print("AVG(" + column + ")\n" + str(average))

"""
maxFromTable(commandArray)

-   Returns the maximum value of a given column for a given table (assuming integers)

"""
def maxFromTable(commandArray):
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

    #   Close the file
    file.close()

    #   Find the column from the table that we are getting the average of
    column = commandArray[1][4 : -1]

    #   Pull the headers from the table
    headers = allLines[0]

    #   Split the headers into an array
    headers = headers.split(" | ")

    #   Initialize an index for the index of the column from the command input
    colIndex = -1

    #   Go through each header, find the index of the column from the command input
    for i in range(len(headers)):
        if headers[i].startswith(column): colIndex = i

    #   Initialize a sum variable for the sum of all column values
    max = 0
    
    #   Iterate through each line, checking if each value is bigger than the max
    #   If the value is bigger than the max, replace the max with the value
    for i in range(len(allLines)):
        if i == 0: continue

        line = allLines[i]

        line = line.split(" | ")

        val = int(line[colIndex])

        if val > max: max = val

    #   Print the average
    return print("MAX(" + column + ")\n" + str(max))

"""
selectAllFromTable(commandArray)

- Called when command begins with "SELECT *"
- Calculates the path to the database using the current working directory, database name, and table name
- Reads each line form the text file and prints it to the terminal

"""
def selectAllFromTable(commandArray):
    #   Handle selecting from multiple tables with a join
    if len(commandArray) > 4: return selectAllFromTwoTables(commandArray)

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
selectAllFromTwoTables(commandArray)

- Reads lines from 2 different tables
- Evalues the condition on columns from 2 different tables
- Uses a nested for loop to check each value from the first table against the second
- Prints the all the columns from the joined tables that make the condition true (unless outer join is specified)

"""
def selectAllFromTwoTables(commandArray):
    #   Remove any commas and semicolons from the command parameters
    for i in range(len(commandArray)): commandArray[i] = commandArray[i].replace(",", "").replace(";", "")

    #   Check if the select is an outer join by looking for the word "outer"
    isOuterJoin = "outer" in commandArray

    #   Check if the select is a left outer join by checking for "outer" and "left"
    isLeftOuterJoin = isOuterJoin and "left" in commandArray

    #   Get the index of "from" from the array of commands
    fromIndex = commandArray.index("from")

    #   Get the name of the first table
    table1Name = commandArray[fromIndex + 1]

    #   The index position of the second table name depends on the type of join and other parameters in the command
    if commandArray[fromIndex + 3] == 'inner': table2Name = commandArray[fromIndex + 5]
    elif commandArray[fromIndex + 3] == 'left': table2Name = commandArray[fromIndex + 6]
    else: table2Name = commandArray[fromIndex + 3]

    #   Find the index of the "where" or "or" keyword (both mean the same thing in this case)
    try: condIndex = commandArray.index("where")
    except: condIndex = commandArray.index("on")

    #   Get the column name of the left hand side of the "where" condition
    table1CondVar = commandArray[condIndex + 1].split(".")[1]

    #   Get the column name of the right hand side of the "where" condition
    table2CondVar = commandArray[condIndex + 3].split(".")[1]

    #   Get the operator of the "where" condition
    operator = commandArray[condIndex + 2]

    #   Get the file path to the first table
    table1Path = getPath(selectedDatabase, table1Name)

    #   Open the file
    table1File = open(table1Path, 'r')

    #   Read all the lines from the file
    table1Rows = table1File.readlines()

    #   Close the file
    table1File.close()

    #   Get the path to the second table's file
    table2Path = getPath(selectedDatabase, table2Name)

    #   Open the second table's file
    table2File = open(table2Path, 'r')

    #   Read all the lines from the second table's file
    table2Rows = table2File.readlines()

    #   Close the second table's file
    table2File.close()

    #   Get an array of the columns from the first table
    table1Cols = table1Rows[0].split(" | ")

    #   Find the index in the array of columns that matches the column from the "where" condition
    for i in range(len(table1Cols)):
        table1ColName = table1Cols[i].split(" ")[0]
        table1ColType = table1Cols[i].split(" ")[1]
        if table1ColName == table1CondVar:
            table1CondVarIndex = i
            table1CondVarType = table1ColType
            break
    
    #   Get an array of the columns from the second table
    table2Cols = table2Rows[0].split(" | ")

    #   Find the index in the array of columns that matches the column from the "where" condition
    for i in range(len(table2Cols)):
        table2ColName = table2Cols[i].split(" ")[0]
        table2ColType = table2Cols[i].split(" ")[1]
        if table2ColName == table2CondVar:
            table2CondVarIndex = i
            table2CondVarType = table2ColType
            break

    #   Concatenate the columns of both tables
    colJoin = table1Rows[0].replace("\n", "") + " | " + table2Rows[0].replace("\n", "")

    #   Create a variable that holds the lines we will print
    shouldPrint = [colJoin]

    #   Iterate through each row in the first table,
    #   then for each row in the second table,
    #   check if the condition is true when evaluating the column from the first table
    #   with the value from the second table.
    #   Then, for each row in the first table, check if there was a match
    #   with any row from the second table,
    #   If not and it's a left outer join, we still print the row from the first table,
    #   and print null (empty) values for the second table
    for i in range(len(table1Rows)):
        if i == 0: continue
        foundMatch = False
        table1RowSplit = table1Rows[i].split(" | ")
        for j in range(len(table2Rows)):
            if j == 0: continue
            table2RowSplit = table2Rows[j].split(" | ")
            if evalCond(table1RowSplit[table1CondVarIndex], operator, table2RowSplit[table2CondVarIndex], table1CondVarType):
                shouldPrint.append(table1Rows[i].replace("\n", "") + " | " + table2Rows[j].replace("\n", ""))
                foundMatch = True
        
        if isLeftOuterJoin and not foundMatch:
                toPrint = table1Rows[i].replace("\n", "")
                for k in range(len(table2Cols)): toPrint += " | "
                shouldPrint.append(toPrint)

    #   Print each line we added to the array from above
    for line in shouldPrint: print(line)


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

-   Adds a new row to the table

"""
def insertInto(tableName, params):
    # Get the table's path
    path = getPath(selectedDatabase, tableName)

    # If table does not exist, return
    if not os.path.exists(path): return print("That table does not exist.")

    #   Re-join params that were previously split by space
    params = ' '.join(params)

    #   Find the index of the first parenthesis
    parenIndex = params.index("(")

    #   Add a space between the parenthesis and the table name
    if params[parenIndex - 1] != " ":
        params = params[:parenIndex] + " " + params[parenIndex:]

    #   Remove 'values(' from beginning of string and ')' from end of string
    params = params[8 : len(params) - 1]

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

    if commandArray[1].lower() == 'database': return createDatabase(commandArray[2])

    if len(commandArray) > 4 and commandArray[1].lower() == 'table': return createTable(commandArray)

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

-   Handles commands that begin with "select"
-   If using 'select *', calls selectAllFromTable(commandArray) function
-   Otherwise, handles filtered select statement by only selecting/printing specified columns that match the condition

"""
def select(commandArray):
    #   If no selectedDatabase, return
    if not selectedDatabase: return print("No database selected.")

    #   If command arguments not greater than 4, command is invalid
    if len(commandArray) < 4: return print("Invalid command.")

    #   If the command uses the COUNT() function, call the handling function
    if commandArray[1].lower().startswith('count'): return countFromTable(commandArray)

    #   If the command uses the AVG() function, call the handling function
    if commandArray[1].lower().startswith('avg'): return avgFromTable(commandArray)

    #   If the command uses the MAX() function, call the handling function
    if commandArray[1].lower().startswith('max'): return maxFromTable(commandArray)

    #   If using 'select *', call a different function to print all rows/columns
    if commandArray[1] == "*": return selectAllFromTable(commandArray)

    #   Get the index of the word "from" in the command
    fromIndex = commandArray.index("from")

    #   The column names we are selected will start at index 1 and end right before the fromIndex
    selectedCols = commandArray[1 : fromIndex]

    #   Remove any whitespace or commas from each selected columns
    for i in range(len(selectedCols)): selectedCols[i] = selectedCols[i].replace(',', '').strip()

    #   Init an array to store the column indexes of the columns that are selected
    selectedColsIndexes = []

    #   Pull the table name form the commandArray
    tableName = commandArray[fromIndex + 1]

    #   Calculate the path to the table using the selected database and the table name
    path = getPath(selectedDatabase, tableName)

    #   If the path does not exist, return
    if not os.path.exists(path): return print("That database or table name does not exist.")

    #   Open the file
    file = open(path)

    #   Read all the lines from the file
    lines = file.readlines()

    #   Close the file
    file.close()

    #   Split first row (the row containing column names) by ' | '
    headers = lines[0].split(' | ')

    #   Find the index in the headers array of each of the selected column names
    #   This will be used to get values from the following rows
    for i in range(len(headers)):
        for j in range(len(selectedCols)):
            if selectedCols[j] in headers[i]: selectedColsIndexes.append(i)

    #   Get the index of the word "where" in the command arguments
    whereIndex = commandArray.index("where")

    #   This is the column name of the 'where' clause
    whereCol = commandArray[whereIndex + 1]

    #   Conditon operator in the where statement
    whereColCond = commandArray[whereIndex + 2]

    #   This is the value of the column name in the 'where' clause
    whereColVal = commandArray[whereIndex + 3].replace('\'', '')

    #   This is the index of the column name in the 'where' clause
    whereColIndex = None

    #   This is the 'type' of the whereColIndex value
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

        #   Print if it's the first row or the 'where' condition is satisfied
        shouldPrint = i == 0 or evalCond(lineArray[whereColIndex], whereColCond, whereColVal, whereColType)

        #   If above condition is not satisfied, continue
        if not shouldPrint: continue

        #   Init an array of values to print for the line
        toPrint = []

        #   Add each selectedColumn value from the row to the array of values to print
        for i in range(len(selectedColsIndexes)):
            toPrint.append(lineArray[selectedColsIndexes[i]].strip())

        #   Re-join the values and print the row to the terminal
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

    if commandArray[1].lower() == 'into': return insertInto(commandArray[2], commandArray[3 : len(commandArray)])

"""
update(commandArray)

-   Change a value of a column in a table
-   Reads the lines, modifies the necessary values, and writes them back to the text file

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

    newPath = None

    #   If the path does not exist, return
    if not os.path.exists(path): return print("That table does not exist.")

    #   Handle pending transactions
    global transactionId
    global transactions

    #   If a transaction is started
    if transactionId:
        #   Check if the table is locked or add to lockedTables.txt file
        if tableLocked(tableName): return print("Error: Table", tableName, "is locked!")

        #   Create a path for a temporary file with the updated data from the transaction
        newPath = getPath(selectedDatabase, tableName + transactionId)

        #   Set a key/value in the dictionary with the key being the original file path and the value being the temporary file path
        transactions[path] = newPath

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
        needsUpdate = lineArray[whereColIndex] == whereColVal

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
    #   If a transaction is in progress, write to the temp file
    #   Else write to the original file
    file = open(newPath if newPath else path, 'w')

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

-   Removes a row from the table

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
    
    confirmation = str(recordsModified) + ' record' + ('s' if recordsModified != 1 else '') + ' deleted.'
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
    validFunctionName = functionName in ['create', 'drop', 'use', 'select', 'alter', 'insert', 'update', 'delete', 'begin', 'commit']

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
    if terminal.lower() == '.exit':
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