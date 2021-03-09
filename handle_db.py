''' 
    This module includes all the database managements required for KeepSafe - Password Manager
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''

import sqlite3, os, io
import encryption as crypt

dbFile = 'keepsafe.db' # Database name
rPath = 'resources'
global pswd, passChanged
pswd = ""   #The current MasterPassword, Changes after the user logins
passChanged = False

if not os.path.exists(rPath):
    os.makedirs(rPath)

DATABASE = os.path.join(rPath, dbFile)

def create_DB(category): # Category is the name of the tables

    '''This function creates a database for KeepSafe Application'''
    get_DB = sqlite3.connect(DATABASE) 

    #IF empty table, then just create the database file and return without creating any tables/category
    if category == "":
        return
    else:
        getCurser = get_DB.cursor()
            # Create table
        getCurser.execute(f'CREATE TABLE {category}(username text, password text)')
        get_DB.commit()
        get_DB.close()

def getTables():
    tables = []
    if(not(os.path.exists(DATABASE))):
        create_DB("")   # Creates a blank database without any tables
    get_DB = sqlite3.connect(DATABASE)
    getCurser = get_DB.cursor()
    try:
        getCurser.execute('SELECT name from sqlite_master where type= "table"')
        items = getCurser.fetchall() #Get all Tables in the database
        for item in items:
            tables.append(item[0])  # Stores the tables in an array
        return tables   # Returns the array of table names
    except:
        raise RuntimeError("Something's not right")

def addElements(category, username, passwd):
    global pswd
    '''Adds elements to database, pass arguements: category, username and password'''
    if(not(os.path.exists(DATABASE))):
        create_DB("")   # Creates a blank database without any tables

    # Encrypting the plain password
    passwd = crypt.encryptData(bytes(passwd, 'utf-8'), pswd).decode()
    get_DB = sqlite3.connect(DATABASE)
    getCurser = get_DB.cursor()

    try:
        getCurser.execute(f"INSERT INTO {category} VALUES ('%s','%s')"%(username,passwd))
        get_DB.commit()
        get_DB.close()
        return "success"
    except sqlite3.OperationalError as err:
        raise RuntimeError(err)
    
            # typeofdata: Either username or password string
            # currentvalue is the current username or password
def modifyElements(category, typeofdata, currentvalue, newvalue):
    '''Edit/Modifys elements from database, pass arguements: category, username and password'''
    global pswd
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')   # Handles FileNotFoundError
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        if typeofdata == 'username':
            try:
                getCurser.execute(f'UPDATE {category} SET username=("%s") WHERE username=("%s")'%(newvalue,currentvalue))
                get_DB.commit()
                get_DB.close()
                return "success"
            except sqlite3.OperationalError as err:
                raise RuntimeError(err)
        elif typeofdata == 'password':
            try:
                getCurser.execute(f'UPDATE {category} SET password=("%s") WHERE password=("%s")'%(newvalue,currentvalue))
                get_DB.commit()
                get_DB.close()
                return "success"
            except sqlite3.OperationalError as err:
                raise RuntimeError(err)
def getA_Password(category, theUser):
    '''This functioon returns the current password of a user depending upon the username'''
    fields = []
    get_DB = sqlite3.connect(DATABASE)
    getCurser = get_DB.cursor()

    try:
        for rows in getCurser.execute(f'SELECT * FROM {category} WHERE username=("%s")'%(theUser)):
            fields = rows[1]
        return fields
    except sqlite3.OperationalError as err:
        raise RuntimeError(err)


def updateHASH(category, theUser, oldPassword):
    '''Updates the passwords in the database if the user changes the Master Password'''
    global pswd
    currentPasswordHash = getA_Password(category, theUser)

    #                 Encrypting the new password with then new user-password
    currentPassword = crypt.decryptData(bytes(currentPasswordHash, 'utf-8'), oldPassword).decode() #Get the plain text password from the encrypted-password
    newPasswordHash = crypt.encryptData(bytes(currentPassword, 'utf-8'), pswd).decode() #Encrypting the new password
    #
    #                 Updating the encrypted password
    #
    get_DB = sqlite3.connect(DATABASE)
    getCurser = get_DB.cursor()
    try:
        getCurser.execute(f'UPDATE {category} SET password=("%s") WHERE username=("%s")'%(newPasswordHash,theUser))
        get_DB.commit()
        get_DB.close()
        return "success"
    except sqlite3.OperationalError as err:
        raise RuntimeError(err)

def delElements(category, username):
    '''Deletes elements from database, pass arguements: category and username'''
    global pswd
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')   # Handles FileNotFoundError
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        try:
            getCurser.execute(f'DELETE FROM {category} WHERE username=("%s")'%username)
            get_DB.commit()
            get_DB.close()
            return "success"
        except sqlite3.OperationalError as err:
            raise RuntimeError(err)

def delTable(category):
    '''This function is responsible for deleting a table from an existing database'''
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        try:
            getCurser.execute(f'DROP TABLE {category}')
            get_DB.commit()
            get_DB.close()
            return "success"
        except sqlite3.OperationalError as err:
            raise RuntimeError(err)

def getElements(category):
    '''Returns a dictionary of elements from database, pass arguements: category'''
    global pswd
    f = []
    fields = {}
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')   # Handles FileNotFoundError
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        try:
            for row in getCurser.execute(f'SELECT * FROM {category}'):
                f.append(row)

            # Preparing Key: Value pairs of Username and Passwords 
            for arrays in f:  
                i = 0       # To avoid repeatation
                for field in arrays:
                    if i == 0:
                        userID = str(field)
                    if i == 1:
                        passVal = str(field)
                        i=0
                        fields.__setitem__(userID, passVal)
                    i += 1
                    
            get_DB.close()
            return fields # Returning the key value pairs of username: passwords
        except sqlite3.OperationalError as err:
            raise RuntimeError(err)
